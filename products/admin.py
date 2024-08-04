from django.contrib import admin

from products.models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    exclude = ('slug',)
    list_display = ('title', 'slug')
    search_fields = ('title', 'slug')
    list_filter = ('title', 'created_at')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    exclude = ('slug',)
    list_display = ('name', 'price', 'discount', 'created_at')
    search_fields = ('name', 'slug',)
    list_filter = ('price', 'created_at')
