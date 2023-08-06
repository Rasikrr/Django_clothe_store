from django.shortcuts import render, HttpResponse
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Categories, Product
from .forms import ProductFilterForm


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
    products = Product.objects.filter(sex="man")
    forms = ProductFilterForm(request.GET)
    size_filter = request.GET.get('size')
    sort_filter = request.GET.get('sort')
    if size_filter:
        products = products.filter(productsize__size=size_filter)
    print(size_filter)
    if sort_filter == 'Ascending Price':
        print("YES")
        products = products.order_by('price')
    elif sort_filter == 'Descending Price':
        products = products.order_by('-price')
    return render(request, "men_outwear.html", context={"products": products,
                                                        "forms": forms,
                                                            })


def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, "single-product.html", context={"product": product, })
