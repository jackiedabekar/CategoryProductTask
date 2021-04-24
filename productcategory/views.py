from django.core.checks.messages import Critical
from django.db.models.query import QuerySet
from .models import Product, Category
from rest_framework.generics import ListCreateAPIView, CreateAPIView
from .serializers import CategorySerializer, ProductSerializer, CategoryProductSerializer, BulkUploadCategoryProductSerializer
from .bulk import check_for_csv
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser, FileUploadParser
import csv
from django.db import transaction
from django.http import HttpResponse

class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all().order_by('-id')
    serializer_class = CategorySerializer


class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerializer

class CategoryProductListAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryProductSerializer

class ProductBulkUpload(CreateAPIView):
    parser_classes = [FormParser, MultiPartParser, JSONParser, FileUploadParser]
    queryset = Product.objects.none()
    serializer_class = BulkUploadCategoryProductSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        failed = []
        file_data = check_for_csv(self, request)
        csv_file = (data.decode('utf-8') for data in file_data)
        reader = csv.DictReader(csv_file)
        all_product = Product.objects.all().select_related('category_name')
        for line in reader:
            check_for_data = all_product.filter(product_name=line['Product'], 
                                                    category_name__category_name=line['Category'])
            if check_for_data:
                line['Message'] = 'Already Exist'
                line['Error'] = 'Product With Name {0} In Category {1} Already Exits'.format(line['Product'],
                                                                                                line['Category'])
                failed.append(line)
                
            if not check_for_data:
                category, created = Category.objects.get_or_create(category_name=line['Category'])
                Product.objects.create(product_name=line['Product'],category_name=category)  
        # if (len(failed) > 0):
        #     response = HttpResponse(content_type='text/csv')
        #     writer = csv.writer(response)
        #     response['Content-Disposition'] = 'attachment; filename="FailedPorductCategory.csv"'
        #     writer.writerow(['Product', 'Category', 'Message', 'Error'])
        #     for fail in failed:
        #         writer.writerow(
        #             [fail['Product'], fail['Category'], fail['Message'], fail['Error']])
        return Response(status=status.HTTP_201_CREATED , data = [{"message": "File Uploaded Successfully."}, 
                                                                                {'duplicate-data': failed}])





