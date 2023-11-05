from django.urls import path
from .import views


urlpatterns = [
    path('', views.marketplace, name='marketplace'),
    path('<slug:vendor_slug>/', views.vendor_detail, name='vendor_detail'),

    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart')

]
