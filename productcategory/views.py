from django.core.checks.messages import Critical
from django.db.models.query import QuerySet
from .models import Product, Category
from rest_framework.generics import ListCreateAPIView, ListAPIView
from .serializers import CategorySerializer, ProductSerializer, CategoryProductSerializer
from django.db.models import Q

class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all().order_by('-id')
    serializer_class = CategorySerializer


class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerializer

class CategoryProductListAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryProductSerializer

    # def get_queryset(self):
    #     queryset = Category.objects.all()
    #     product = self.request.GET.get('product')
    #     category = self.request.GET.get('category')
    #     print(category, product, queryset)
    #     q_obhect = Q()
    #     if product or category:
    #         queryset.filter(category_name__icontains=category)
    #     return queryset




