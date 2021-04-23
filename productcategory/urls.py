from django.urls import path, re_path
from .views import CategoryListCreateAPIView, ProductListCreateAPIView, CategoryProductListAPIView

app_name = 'productcategory'

urlpatterns = [
    path('product/', ProductListCreateAPIView.as_view(), name='all-product-list'),
    path('category/', CategoryListCreateAPIView.as_view(), name='all-category-list'),
    path('allcat/', CategoryProductListAPIView.as_view(), name='all-cat-prod')
]