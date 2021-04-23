from django.db import models
from rest_framework import serializers
from .models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    '''
    This Is Category Serilaizer To Serialize All 
    The Fields Of Category Model
    '''
    class Meta:
        model = Category
        fields = ['id','category_name']

class ProductSerializer(serializers.ModelSerializer):
    '''
    This Is Product Serilaizer To Serialize All 
    The Fields Of Product Model, with Extra Field To Display
    Its Category
    '''
    category = serializers.CharField(source='category_name')
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'category']

class ProductForImportSerializer(serializers.ModelSerializer):
    '''
    An Dummy Product Serializer Without Category Field
    '''
    class Meta:
        model = Product
        fields = ['id', 'product_name']

class CategoryProductSerializer(serializers.ModelSerializer):
    '''
    An Category Plus Product Serializer To Display All
    Product Belong To Particular Category
    '''
    product = ProductForImportSerializer(many=True, source='product_set')
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'product']

