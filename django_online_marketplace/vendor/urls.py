from django.urls import path, include
from . import views
from accounts import views as AccountViews


urlpatterns = [
    path('', AccountViews.vendordashboard,name='vendor'),
    path('profile/',views.vendorprofile, name='vendorprofile'),
    path('menu-builder/', views.menu_builder,name='menu-builder'),

]
