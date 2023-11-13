from django.urls import path, include
from . import views
from accounts import views as AccountViews


urlpatterns = [
    path('', AccountViews.vendordashboard,name='vendor'),
    path('profile/',views.vendorprofile, name='vendorprofile'),
    path('menu-builder/', views.menu_builder, name='menu-builder'),
    path('menu-builder/category/<int:pk>/', views.products_by_category,name='products_by_category'),

    #CATEGORY CRUD
    path('menu-builder/category/add',views.add_category, name='add_category'),
    path('menu-builder/category/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('menu-builder/category/delete/<int:pk>/', views.delete_category, name='delete_category'),

    #PRODUCT CRUD
    path('menu-builder/product/add',views.add_product,name='add_product'),
    path('menu-builder/product/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('menu-builder/product/delete/<int:pk>/', views.delete_product, name='delete_product'),

    #OPENING HOURS
    path('opening-hours/', views.opening_hours, name='opening_hours'),
    path('opening-hours/add/', views.add_opening_hours, name='add_opening_hours'),
    path('opening-hours/remove<int:pk>/',views.remove_opening_hours,name='remove_opening_hours'),

]
