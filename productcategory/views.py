from django.core.checks.messages import Critical
from django.db.models.query import QuerySet
from .models import Product, Category
from rest_framework.generics import ListCreateAPIView, ListAPIView
from .serializers import CategorySerializer, ProductSerializer, CategoryProductSerializer

class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all().order_by('-id')
    serializer_class = CategorySerializer


class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerializer

class CategoryProductListAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryProductSerializer




