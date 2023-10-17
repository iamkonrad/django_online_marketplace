from django.shortcuts import render, redirect

from vendor.forms import VendorForm
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages, auth


def registeruser(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data ['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email = email,
                                            password=password)
            user.role = 2
            user.save()
            messages.success(request, 'Your account has been successfully registered.')
            return redirect('registeruser')
        else:
            print('invalid form')
            print(form.errors)
    else:
        form = UserForm()
    context = {
        'form':form,
    }
    return render(request, 'accounts/registeruser.html', context)


def registervendor(request):
    if request.method =='POST':
        form = UserForm(request.POST)
        vendor_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and vendor_form.is_valid:
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email,
                                            password=password)
            user.role = 1
            user.save()
            vendor = vendor_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, 'Your vendor account has been successfully registered.')
            return redirect('registervendor')
        else:
            print('invalid form')
            print(form.errors)

    else:
        form = UserForm()
        vendor_form = VendorForm()

    context = {
        'form':form,
        'vendor_form':vendor_form,
    }

    return render (request, 'accounts/registervendor.html', context)


def login (request):
    if request.method =='POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You have been logged-in.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials.')
            return redirect('login')
    return render (request, 'accounts/login.html')

def logout (request):
    auth.logout(request)
    messages.info(request,'You are now logged-out.')
    return redirect ('login')

def dashboard (request):
    return render (request, 'accounts/dashboard.html')