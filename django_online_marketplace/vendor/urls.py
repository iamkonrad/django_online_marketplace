from django.urls import path, include
from . import views
from accounts import views as AccountViews


urlpatterns = [
    path('', AccountViews.vendordashboard,name='vendor'),
    path('profile/',views.vendorprofile, name='vendorprofile'),
    path('menu-builder/', views.menu_builder, name='menu-builder'),
    path('menu-builder/category/<int:pk>/', views.products_by_category,name='products_by_category'),

    path('menu-builder/category/add',views.add_category, name='add_category'),

]
