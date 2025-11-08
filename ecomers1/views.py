from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .models import Category, Brand, Goods, Basket, Order, OrderItem
from .forms import RegisterForm


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'registration.html'
    success_url = reverse_lazy('login')


class GoodsListView(ListView):
    model = Goods
    template_name = 'goods_list.html'
    context_object_name = 'goods'
    paginate_by = 10

    def get_queryset(self):
        qs = Goods.objects.all().select_related('category', 'brand')
        category_id = self.request.GET.get('category')
        brand_id = self.request.GET.get('brand')
        q = self.request.GET.get('q')
        if category_id:
            try:
                qs = qs.filter(category_id=int(category_id))
            except (ValueError, TypeError):
                pass
        if brand_id:
            try:
                qs = qs.filter(brand_id=int(brand_id))
            except (ValueError, TypeError):
                pass
        if q:
            qs = qs.filter(name__icontains=q)
        return qs.order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['brands'] = Brand.objects.all()
        context['selected_category'] = self.request.GET.get('category', '')
        context['selected_brand'] = self.request.GET.get('brand', '')
        context['search_q'] = self.request.GET.get('q', '')
        return context


class GoodsDetailView(DetailView):
    model = Goods
    template_name = 'goods_detail.html'
    context_object_name = 'goods'


class BasketListView(ListView):
    model = Basket
    template_name = 'basket.html'
    context_object_name = 'basket'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Basket.objects.filter(user=self.request.user)
        return Basket.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        basket = self.get_queryset()
        context['total'] = sum(item.goods.price.amount * item.quantity for item in basket)
        return context


@method_decorator(login_required, name='dispatch')
class AddToBasketView(View):
    def get(self, request, pk):
        goods = get_object_or_404(Goods, pk=pk)
        basket_item, created = Basket.objects.get_or_create(user=request.user, goods=goods)
        basket_item.quantity += 1
        basket_item.save()
        return redirect(request.META.get('HTTP_REFERER', 'goods_list'))


@method_decorator(login_required, name='dispatch')
class RemoveFromBasketView(View):
    def get(self, request, pk):
        basket_item = get_object_or_404(Basket, pk=pk, user=request.user)
        basket_item.delete()
        return redirect('basket_view')



@method_decorator(login_required, name='dispatch')
class IncreaseQuantityView(View):
    def get(self, request, pk):
        basket_item = get_object_or_404(Basket, pk=pk, user=request.user)
        basket_item.quantity += 1
        basket_item.save()
        return redirect('basket_view')



@method_decorator(login_required, name='dispatch')
class DecreaseQuantityView(View):
    def get(self, request, pk):
        basket_item = get_object_or_404(Basket, pk=pk, user=request.user)
        if basket_item.quantity > 1:
            basket_item.quantity -= 1
            basket_item.save()
        else:
            basket_item.delete()
        return redirect('basket_view')


@method_decorator(login_required, name='dispatch')
class CreateOrderView(View):
    def get(self, request):
        basket_items = Basket.objects.filter(user=request.user)
        if not basket_items.exists():
            return redirect('basket_view')
        return render(request, 'order_form.html')

    def post(self, request):
        basket_items = Basket.objects.filter(user=request.user)
        if not basket_items.exists():
            return redirect('basket_view')

        recipient_name = request.POST.get('recipient_name')
        address = request.POST.get('address')
        card_number = request.POST.get('card_number')

        total = sum(item.goods.price.amount * item.quantity for item in basket_items)
        order = Order.objects.create(user=request.user, total_price=total)

        for item in basket_items:
            OrderItem.objects.create(
                order=order,
                goods=item.goods,
                quantity=item.quantity,
                price=item.goods.price.amount
            )

        basket_items.delete()

        return render(request, 'order_success.html', {
            'order': order,
            'recipient_name': recipient_name,
            'address': address,
            'card_number': f"**** **** **** {card_number[-4:]}"
        })
