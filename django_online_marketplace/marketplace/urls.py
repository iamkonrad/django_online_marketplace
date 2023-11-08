from django.urls import path
from .import views


urlpatterns = [
    path('', views.marketplace, name='marketplace'),
    path('<slug:vendor_slug>/', views.vendor_detail, name='vendor_detail'),


    # CART
    #CRUD
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('decrease_cart/<int:product_id>/', views.decrease_cart, name='decrease_cart'),
    path('delete_cart/<int:cart_id>/', views.delete_cart, name='delete_cart'),

    #View
    path('cart/', views.cart, name='cart'),
]