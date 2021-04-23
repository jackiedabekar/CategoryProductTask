from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length = 100, null=False, blank=False)

    def __str__(self):
        return self.category_name

class Product(models.Model):
    category_name = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length = 100, null=False, blank=False)

    def __str__(self):
        return self.product_name    
    
    
