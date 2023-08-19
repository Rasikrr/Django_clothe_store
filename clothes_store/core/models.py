from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()


class Profile(models.Model):
    COUNTRIES = [
        ("Kazakhstan", "Kazakhstan"),
        ("Russia", "Russia"),
        ("Germany", "Germany"),
        ("USA", "USA"),
        ("China", "China"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="profile_images", default="img-profile-default.png")
    country = models.CharField(max_length=50, choices=COUNTRIES)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=100)
    mail_index = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.user.email}"


class Categories(models.Model):
    name = models.CharField(max_length=100)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='subcategories')

    def __str__(self):
        return self.name


class Product(models.Model):
    SEX_CHOICES = [
        ("man", "man"),
        ("woman", "woman")
    ]
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to="product_images")
    sex = models.CharField(max_length=5, choices=SEX_CHOICES)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ProductSize(models.Model):
    SIZE_CHOICES = [
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=5, choices=SIZE_CHOICES)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - {self.size}"


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"User: {self.user.username},Item: {self.product_id.product.name} {self.product_id.size}"


class Subscribe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    used = models.BooleanField()

    def __str__(self):
        return f"{self.name} {self.email}"

