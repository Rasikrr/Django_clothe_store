from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Categories, Product, ProductSize, Profile, CartItem, Subscribe
from .forms import ProductFilterForm, OutwearFilterForm
from random import sample


def index(request):
    try:
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)
    except User.DoesNotExist:
        user_profile = ""
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        user_object = User.objects.get(username=request.user.username)
        if Subscribe.objects.filter(user=user_object, email=email).exists():
            messages.info(request, "Subscriber with this email is exists")
            return redirect("index")
        subscriber = Subscribe.objects.create(name=name, email=email, user=user_object, used=False)
        subscriber.save()
        return redirect("index")
    else:
        men_products = sample(list(Product.objects.filter(sex="man")), k=4)
        women_products = sample(list(Product.objects.filter(sex="woman")), k=4)
        try:
            User.objects.get(username=request.user.username)
            if Subscribe.objects.filter(user=user_object).exists():
                show = False
            else:
                show = True
        except User.DoesNotExist:
            show = False
        return render(request, "index.html", context={"men_products": men_products,
                                                      "user_profile": user_profile,
                                                      "women_products": women_products,
                                                      "show": show
                                                     })


def signup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password_1 = request.POST.get("password_1")
        password_2 = request.POST.get("password_2")
        policy = request.POST.get("policy")
        if password_1 == password_2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "User with this email is exists")
                return redirect("signup")
            elif User.objects.filter(username=name).exists():
                messages.info(request, "User with this username is exists")
                return redirect("signup")
            else:
                if policy:
                    user = User.objects.create_user(username=name, email=email, password=password_1)
                    user.save()
                    user_login = auth.authenticate(username=name, password=password_1, email=email)
                    auth.login(request, user_login)

                    # Create profile
                    user_model = User.objects.get(email=email)
                    new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                    new_profile.save()
                    print("HERE")
                    return redirect("index")
                else:
                    messages.info(request, "Please accept policy")
                    return redirect("signup")

        else:
            messages.info(request, "Passwords are not similar")
            return redirect("signup")
    else:
        return render(request, "signup.html")


def signin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("index")
        else:
            messages.info(request, "email or password is incorrect")
            return redirect("signin")
    else:
        return render(request, "signin.html")


@login_required(login_url="signin")
def profile(request, id_user):
    user_profile = Profile.objects.get(id_user=id_user)
    if request.method == "POST":
        first_name = request.POST.get("first-name")
        last_name = request.POST.get("last-name")
        image = request.FILES.get("image")
        if image:
            user_profile.image = image
        country = request.POST.get("country")
        city = request.POST.get("city")
        street = request.POST.get("street")
        mail_index = request.POST.get("mail-index")
        user_profile.first_name = first_name
        user_profile.last_name = last_name
        user_profile.country = country
        user_profile.city = city
        user_profile.street = street
        user_profile.mail_index = mail_index
        user_profile.save()
        return redirect("profile", id_user=id_user)
    else:
        country_choice = Profile.COUNTRIES
        return render(request, "profile.html", context={"user_profile": user_profile,
                                                        "country_choice": country_choice
                                                        })


def men(request):
    try:
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)
    except User.DoesNotExist:
        user_profile = ""
    products = sample(list(Product.objects.filter(sex="man")), k=12 )
    print(products)
    return render(request, "men.html", context={"products": products,
                                                "user_profile": user_profile
                                                })


def women(request):
    try:
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)
    except User.DoesNotExist:
        user_profile = ""
    products = sample(list(Product.objects.filter(sex="woman")), k=3)
    return render(request, "women.html", context={"products": products,
                                                  "user_profile": user_profile
                                                  })


def contact(request):
    try:
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)
    except User.DoesNotExist:
        user_profile = ""
    return render(request, "contact.html", context={"user_profile": user_profile})


def about(request):
    try:
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)
    except User.DoesNotExist:
        user_profile = ""
    return render(request, "about.html", context={"user_profile": user_profile})


def men_outwear(request):
    try:
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)
    except User.DoesNotExist:
        user_profile = ""
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
                                                        "user_profile": user_profile
                                                        })


def women_outwear(request):
    try:
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)
    except User.DoesNotExist:
        user_profile = ""
    parent_category = Categories.objects.get(name="Outwear")
    all_outwear = Categories.objects.filter(parent_category=parent_category)
    products = Product.objects.filter(category__in=all_outwear, sex="woman")
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
                                                          "user_profile": user_profile
                                                        })


def men_shirts(request):
    try:
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)
    except User.DoesNotExist:
        user_profile = ""
    parent_category = Categories.objects.get(name="Shirts_polos_t-shirts")
    all_shirts = Categories.objects.filter(parent_category=parent_category)
    products = Product.objects.filter(category__in=all_shirts, sex="man")
    return render(request, "men_shirts.html", context={"products": products,
                                                       "user_profile": user_profile
                                                       })


def product_detail(request, product_id):
    try:
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)
    except User.DoesNotExist:
        user_profile = ""
    product = Product.objects.get(id=product_id)
    sizes = ProductSize.SIZE_CHOICES
    return render(request, "single-product.html", context={"product": product,
                                                           "sizes": sizes,
                                                           "user_profile": user_profile
                                                           })


def search(request):
    try:
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)
    except User.DoesNotExist:
        user_profile = ""
    if request.method == "POST":
        product_name = request.POST.get("product-name")
        products = Product.objects.filter(name__icontains=product_name)
        return render(request, "search.html", context={"user_profile": user_profile,
                                                       "products": products,
                                                       "search": product_name})
    else:
        return render(request, "search.html", context={"user_profile": user_profile,
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


def add_to_cart(request, product_id, product_size):
    if not request.user.is_authenticated:
        return JsonResponse({'message': 'You have to sign in before adding item to cart'})
    user_object = request.user
    product_object = Product.objects.get(id=product_id)
    product = ProductSize.objects.get(product=product_object, size=product_size)
    cart_item, created = CartItem.objects.get_or_create(user=user_object, product_id=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()
    product.quantity -= 1
    product.save()

    return JsonResponse({'message': 'Item added to cart.'})


def remove_from_cart(request, product_id, product_size):
    user_object = request.user
    product_object = Product.objects.get(id=product_id)
    product = ProductSize.objects.get(product=product_object, size=product_size)
    cart_item = CartItem.objects.filter(user=user_object, product_id=product).first()
    cart_item.quantity -= 1
    product.quantity += 1
    quantity = str(cart_item.quantity)
    if cart_item.quantity == 0:
        cart_item.delete()
    else:
        cart_item.save()
    product.save()
    print(quantity)
    return JsonResponse({'quantity': quantity})


@login_required(login_url="signin")
def cart(request, id_user):
    user_profile = Profile.objects.get(id_user=id_user)
    products = CartItem.objects.filter(user=request.user)
    total_price = 0
    for product in products:
        total_price += product.product_id.product.price * product.quantity
    return render(request, "cart.html", context={"user_profile": user_profile,
                                                 "products": products,
                                                 "total_items": len(products),
                                                 "total_price": total_price
                                                })


def check_delivery_data(request, id_user):
    user_profile = Profile.objects.get(id_user=id_user)
    first_name = user_profile.first_name
    last_name = user_profile.last_name
    country = user_profile.country
    city = user_profile.city
    street = user_profile.street
    mail_index = user_profile.mail_index
    data = [first_name, last_name, country, city, street, mail_index]
    if not all(data):
        return JsonResponse({"response": "not full"})
    return JsonResponse({"response": "full"})


def check_total_price(request, total_price):
    if int(total_price) == 0:
        print("YES")
        return JsonResponse({"response": "False"})
    return JsonResponse({"response": "True"})


@login_required(login_url="signin")
def checkout(request):
    user_profile = Profile.objects.get(user=request.user)
    return render(request, "checkout.html", context={"user_profile": user_profile})


@login_required(login_url="signin")
def logout(request):
    auth.logout(request)
    return redirect("index")

