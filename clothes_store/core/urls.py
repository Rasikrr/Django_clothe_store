from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("signup", views.signup, name="signup"),
    path("signin", views.signin, name="signin"),
    path("contactus", views.contact, name="contactus"),
    path("aboutus", views.about, name="aboutus"),
    path("men/", views.men, name="men"),
    path("women/", views.women, name="women"),
    path("men/outwear", views.men_outwear, name="men_outwear"),
    path("women/outwear", views.women_outwear, name="women_outwear"),
    path("men/shirts", views.men_shirts, name="men_shirts"),
    path("product/<int:product_id>/", views.product_detail, name="product_detail"),
    path("search", views.search, name="search"),
    path('get_product_size_info/', views.get_product_size_info, name='get_product_size_info'),
    path("profile/<int:id_user>", views.profile, name="profile"),
    path('add_to_cart/<int:product_id>&<str:product_size>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>&<str:product_size>/', views.remove_from_cart, name='remove_from_cart'),
    path("cart/<int:id_user>", views.cart, name="cart"),
    path("check_delivery_data/<int:id_user>", views.check_delivery_data, name="check_delivery_data"),
    path("checkout", views.checkout, name="checkout"),
    path("logout", views.logout, name="logout")

]