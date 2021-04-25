from .models import Product, Category
from rest_framework.generics import ListCreateAPIView, CreateAPIView, ListAPIView
from .serializers import CategorySerializer, ProductSerializer, CategoryProductSerializer, BulkUploadCategoryProductSerializer
from .bulk import check_for_csv
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser, FileUploadParser
import csv
from django.db import transaction
from .task import do_the_work
from django.db.models import Prefetch


class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all().order_by('-id')
    serializer_class = CategorySerializer


class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerializer

class CategoryProductListAPIView(ListAPIView):
    # queryset = Category.objects.all()
    serializer_class = CategoryProductSerializer

    def get_queryset(self):
        product = self.request.GET.get('product')
        category = self.request.GET.get('category')
        queryset = Category.objects.prefetch_related(
            Prefetch('product_set', Product.objects.all(), to_attr='products')
        )
        if category:
            queryset.filter(category_name__icontains=category)
        if product:
            queryset.filter(product_name__icontains=product)
        return queryset
    

class ProductBulkUpload(CreateAPIView):
    parser_classes = [FormParser, MultiPartParser, JSONParser, FileUploadParser]
    queryset = Product.objects.none()
    serializer_class = BulkUploadCategoryProductSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        # failed = []
        file_data = check_for_csv(self, request)
        csv_file = (data.decode('utf-8') for data in file_data)
        reader = csv.DictReader(csv_file)
        reader = [line for line in reader]
        failed = do_the_work.delay(reader).get()
        # all_product = Product.objects.all().select_related('category_name')
        # for line in reader:
        #     check_for_data = all_product.filter(product_name=line['Product'], 
        #                                             category_name__category_name=line['Category'])
        #     if check_for_data:
        #         line['Message'] = 'Already Exist'
        #         line['Error'] = 'Product With Name {0} In Category {1} Already Exits'.format(line['Product'],
        #                                                                                         line['Category'])
        #         failed.append(line)
                
        #     if not check_for_data:
        #         category, created = Category.objects.get_or_create(category_name=line['Category'])
        #         Product.objects.create(product_name=line['Product'],category_name=category)  
        return Response(status=status.HTTP_201_CREATED , data = [{"message": "File Uploaded Successfully."}, 
                                                                               {'duplicate-data': failed}])
