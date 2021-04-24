from django.urls import path, re_path
from .views import CategoryListCreateAPIView, ProductListCreateAPIView, CategoryProductListAPIView, ProductBulkUpload

app_name = 'productcategory'

urlpatterns = [

    # Endpoint To Display All Product With Their Catrgory
    path('product/', ProductListCreateAPIView.as_view(), name='all-product-list'),
    # Endpoint To Display All Category
    path('category/', CategoryListCreateAPIView.as_view(), name='all-category-list'),
    # Endpoint To Display All Category And Product In Them
    path('allcatprod/', CategoryProductListAPIView.as_view(), name='all-cat-prod'),
    # Endpoint To Upload Product By Category Name Using CSV File
    path('bulkupload/', ProductBulkUpload.as_view(), name='bulk-upload')
]