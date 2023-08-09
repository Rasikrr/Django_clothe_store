from django.urls import path
from . import views


urlpatterns = [
    path("", views.index,name="index"),
    path("signup", views.signup, name="signup"),
    path("signin", views.signin, name="signin"),
    path("contactus", views.contact, name="contactus"),
    path("aboutus", views.about, name="aboutus"),
    path("men/", views.men, name="men"),
    path("women/", views.women, name="women"),
    path("men/outwear", views.men_outwear, name="men_outwear"),
    path("women/outwear", views.women_outwear, name="women_outwear"),
    path("product/<int:product_id>", views.product_detail, name="product_detail"),
    path('get_product_size_info/', views.get_product_size_info, name='get_product_size_info'),

]