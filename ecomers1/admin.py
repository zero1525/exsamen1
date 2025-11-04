from django.contrib import admin
from .models import Category, Brand, Goods, Basket


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'goods_count')
    search_fields = ('name',)
    ordering = ('name',)
    list_display_links = ('id', 'name')

    def goods_count(self, obj):
        return obj.goods_set.count()
    goods_count.short_description = 'Количество товаров'


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'goods_count')
    search_fields = ('name',)
    ordering = ('name',)
    list_display_links = ('id', 'name')

    def goods_count(self, obj):
        return obj.goods_set.count()
    goods_count.short_description = 'Количество товаров'


class BasketInline(admin.TabularInline):
    model = Basket
    extra = 1
    readonly_fields = ('quantity',)
    verbose_name = "Корзина"
    verbose_name_plural = "Корзины, содержащие этот товар"


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'brand')
    list_filter = ('category', 'brand')
    search_fields = ('name', 'description')
    ordering = ('name',)
    list_select_related = ('category', 'brand')
    list_editable = ('price',)
    list_display_links = ('id', 'name')

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'category', 'brand', 'img')
        }),
        ('Цена', {
            'fields': ('price',)
        }),
    )

    inlines = [BasketInline]


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('id', 'goods', 'quantity', 'total_price')
    search_fields = ('goods__name',)
    list_filter = ('goods__category', 'goods__brand')
    list_select_related = ('goods',)
    readonly_fields = ('total_price',)

    def total_price(self, obj):
        return obj.goods.price * obj.quantity
    total_price.short_description = 'Общая стоимость'
