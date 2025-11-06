from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, redirect
from .models import Category, Brand, Goods, Basket
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import RegisterForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


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
                cid = int(category_id)
                qs = qs.filter(category_id=cid)
            except (ValueError, TypeError):
                pass

        if brand_id:
            try:
                bid = int(brand_id)
                qs = qs.filter(brand_id=bid)
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

from django.views import View

@method_decorator(login_required, name='dispatch')
class AddToBasketView(View):
    def get(self, request, pk):
        goods = get_object_or_404(Goods, pk=pk)
        basket_item, created = Basket.objects.get_or_create(user=request.user, goods=goods)
        basket_item.quantity += 1
        basket_item.save()
        return redirect('basket_view')


class RemoveFromBasketView(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            basket_item = get_object_or_404(Basket, pk=pk, user=request.user)
            basket_item.delete()
        return redirect('basket_view')
