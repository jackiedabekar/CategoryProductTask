from django.db import models
from rest_framework import serializers
from .models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','category_name']

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category_name')
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'category']

class ProductForImportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'product_name']

class CategoryProductSerializer(serializers.ModelSerializer):
    product = ProductForImportSerializer(many=True, source='product_set')
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'product']

