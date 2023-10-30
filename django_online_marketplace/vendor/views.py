from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect

from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from accounts.views import check_role_vendor
from menu.forms import CategoryForm, ProductForm
from menu.models import Category, Product
from vendor.forms import VendorForm
from vendor.models import Vendor
from django.contrib import messages
from .utils import get_vendor
from django.template.defaultfilters import slugify




@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST,request.FILES,instance=profile)
        vendor_form = VendorForm(request.POST,request.FILES,instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request,'Your data has been saved. ')
            return redirect('vendorprofile')
        else:
            messages.error(request, 'There was an error. Please try again ')
            return redirect('vendordashboard')

    else:
        profile_form = UserProfileForm(instance = profile)
        vendor_form = VendorForm(instance = vendor)

    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor': vendor,
    }

    return render(request,'vendor/vendorprofile.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')

    context = {
        'categories':categories,
    }

    return render(request,'vendor/menu_builder.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def products_by_category(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category,pk=pk)
    products = Product.objects.filter(vendor=vendor,category=category)

    context = {
        'products': products,
        'category': category,
    }

    return render(request,'vendor/products_by_category.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            category.save()
            messages.success(request,"Category has been added.")
            return redirect('menu-builder')
    else:
        form = CategoryForm()

    context = {
        'form':form,
    }

    return render(request, 'vendor/add_category.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_category(request,pk=None ):
    category = get_object_or_404(Category,pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            category.save()
            messages.success(request,"Category has been updated.")
            return redirect('menu-builder')
    else:
        form = CategoryForm(instance=category)

    context = {
        'form':form,
        'category':category,
    }

    return render(request, 'vendor/edit_category.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_category(request, pk=None):
    category=get_object_or_404(Category,pk=pk)
    category.delete()
    messages.success(request, "Category has been deleted.")
    return redirect('menu_builder')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            product_title = form.cleaned_data['product_title']
            product = form.save(commit=False)
            product.vendor = get_vendor(request)
            product.slug = slugify(product_title)
            product.save()
            messages.success(request, "Product has been added.")
            return redirect('products_by_category', product.category.id)
    else:
        form = ProductForm()
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
    context = {
        'form': form,
    }

    return render(request, 'vendor/add_product.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_product(request, pk=None):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product_title = form.cleaned_data['product_title']
            product = form.save(commit=False)
            product.vendor = get_vendor(request)
            product.slug = slugify(product_title)
            product.save()
            messages.success(request, "Product has been updated.")
            return redirect('products_by_category',product.category.id)
    else:
        form = ProductForm(instance=product)
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))

    context = {
        'form': form,
        'product': product,
    }

    return render(request, 'vendor/edit_product.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_product(request, pk=None):
    product=get_object_or_404(Product,pk=pk)
    product.delete()
    messages.success(request, "Product has been deleted.")
    return redirect('products_by_category', product.category.id)
