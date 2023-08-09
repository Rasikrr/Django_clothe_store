from django.shortcuts import render, HttpResponse
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Categories, Product, ProductSize
from .forms import ProductFilterForm, OutwearFilterForm
from random import sample


def index(request):
    men_products = sample(list(Product.objects.filter(sex="man")), k=4)
    return render(request, "index.html", context={"men_products": men_products,
                                                 })


def signup(request):
    return render(request, "signup.html")


def signin(request):
    return render(request, "signin.html")


def men(request):
    products = sample(list(Product.objects.filter(sex="man")), k=3)
    print(products)
    return render(request, "men.html", context={"products": products})


def women(request):
    products = sample(list(Product.objects.filter(sex="women")), k=3)
    return render(request, "women.html", context={"products": products,
                                                  })


def contact(request):
    return render(request, "contact.html")


def about(request):
    return render(request, "about.html")


def men_outwear(request):
    parent_category = Categories.objects.get(name="Outwear")
    all_outwear = Categories.objects.filter(parent_category=parent_category)
    products = Product.objects.filter(sex="man", category__in=all_outwear)
    forms = OutwearFilterForm(request.GET)
    size_filter = request.GET.get('size')
    sort_filter = request.GET.get('sort')
    if size_filter:
        products = products.filter(productsize__size=size_filter)
    if sort_filter == 'Ascending Price':
        products = products.order_by('price')
    elif sort_filter == 'Descending Price':
        products = products.order_by('-price')
    if forms.is_valid():  # Проверка на валидность формы
        if forms.cleaned_data['type_of_outwear']:
            selected_types = forms.cleaned_data['type_of_outwear']
            products = products.filter(category__name__in=selected_types)

    return render(request, "men_outwear.html", context={"products": products,
                                                        "forms": forms,
                                                        })


def women_outwear(request):
    parent_category = Categories.objects.get(name="Outwear")
    all_outwear = Categories.objects.filter(parent_category=parent_category)
    products = Product.objects.filter(category__in=all_outwear, sex="women")
    forms = OutwearFilterForm(request.GET)
    size_filter = request.GET.get('size')
    sort_filter = request.GET.get('sort')
    if size_filter:
        products = products.filter(productsize__size=size_filter)
    if sort_filter == 'Ascending Price':
        products = products.order_by('price')
    elif sort_filter == 'Descending Price':
        products = products.order_by('-price')
    if forms.is_valid():  # Проверка на валидность формы
        if forms.cleaned_data['type_of_outwear']:
            selected_types = forms.cleaned_data['type_of_outwear']
            products = products.filter(category__name__in=selected_types)

    return render(request, "women_outwear.html", context={"products": products,
                                                        "forms": forms,
                                                        })


def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    sizes = ProductSize.SIZE_CHOICES
    return render(request, "single-product.html", context={"product": product,
                                                           "sizes": sizes,
                                                           })


def get_product_size_info(request):
    if request.method == 'POST':
        product_id = request.GET.get('product_id')
        size = request.POST.get('size')
        if product_id and size:
            try:
                product = Product.objects.get(id=product_id)
                product_size = ProductSize.objects.get(product=product, size=size)
                availability_message = f"In stock: {product_size.quantity}" if product_size.quantity > 0 else "Out of stock"
                return JsonResponse({'availability_message': availability_message, 'max_quantity': product_size.quantity})
            except (Product.DoesNotExist, ProductSize.DoesNotExist):
                pass
    return JsonResponse({'availability_message': 'Out of stock'})