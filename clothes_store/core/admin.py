from django.contrib import admin
from .models import Product, Categories, ProductSize, Profile


# Register your models here.
admin.site.register(Categories)
admin.site.register(Product)
admin.site.register(ProductSize)
admin.site.register(Profile)