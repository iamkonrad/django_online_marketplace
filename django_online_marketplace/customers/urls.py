from django.urls import path
from  accounts import views as AccountViews



urlpatterns = [
    path('', AccountViews.customerdashboard,name='customer'),



]
