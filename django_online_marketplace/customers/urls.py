from django.urls import path
from accounts import views as AccountViews
from . import views


urlpatterns = [
    path('', AccountViews. customerdashboard, name='customer'),
    path('profile/', views.customer_profile, name='customer_profile'),



]
