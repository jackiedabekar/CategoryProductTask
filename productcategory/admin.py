from django.contrib import admin
from .models import Product, Category

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_name', 'category_name']
    list_editable = ('category_name',)

@admin.register(Category)
class CatrgoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_name']
