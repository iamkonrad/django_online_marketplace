from django import forms

from accounts.validators import only_allow_images_validator
from menu.models import Category, Product


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'description']

class ProductForm(forms.ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn-btn-info w-100'}), validators=[only_allow_images_validator])
    class Meta:
        model = Product
        fields = ['category','product_title','description','price','image','is_available']


