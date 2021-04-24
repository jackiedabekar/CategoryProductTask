from celery import shared_task
from .models import Product,Category

@shared_task
def do_the_work(reader):
    failed = []
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
    return failed