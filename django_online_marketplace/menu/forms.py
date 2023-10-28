from django import forms
from menu.models import Category, Product


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'description']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category','product_title','description','price','image','is_available']


