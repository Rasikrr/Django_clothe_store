from django.contrib import admin
from .models import Product, Categories, ProductSize


# Register your models here.
admin.site.register(Categories)
admin.site.register(Product)
admin.site.register(ProductSize)