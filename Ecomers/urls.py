
from django.contrib import admin
from django.urls import path
from Ecomers import settings
from ecomers1.views import GoodsListView, GoodsDetailView, BasketListView, AddToBasketView, RegisterView, RemoveFromBasketView
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', GoodsListView.as_view(), name='goods_list'),
    path('goods/<int:pk>/', GoodsDetailView.as_view(), name='goods_detail'),
    path('add-to-basket/<int:pk>/', AddToBasketView.as_view(), name='add_to_basket'),
    path('basket/', BasketListView.as_view(), name='basket_view'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='goods_list'), name='logout'),
    path('remove-from-basket/<int:pk>/', RemoveFromBasketView.as_view(), name='remove_from_basket'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    