from django.shortcuts import render, HttpResponse
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Categories, Product


def index(request):
    return render(request, "index.html")


def signup(request):
    return render(request, "signup.html")


def signin(request):
    return render(request, "signin.html")


def men(request):
    return render(request, "men.html")


def women(request):
    return render(request, "women.html")


def contact(request):
    return render(request, "contact.html")


def about(request):
    return render(request, "about.html")


def men_outwear(request):
    print("START")
    products = Product.objects.filter(sex="man")
    for product in products:
        print(product.image.url)
    print(1)
    return render(request, "men_outwear.html", context={"products": products,
                                                        })


def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, "single-product.html", context={"product": product, })
