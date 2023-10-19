from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from vendor.forms import VendorForm
from .forms import UserForm
from .utils import detectuser, send_verification_email
from .models import User, UserProfile
from django.contrib import messages, auth

def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied

def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied


def registeruser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already registered!')
        return redirect('customerdashboard')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data ['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email = email,
                                            password=password)
            user.role = User.CUSTOMER
            user.save()


            send_verification_email(request,user)                                                                       #Verification email
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
    if request.user.is_authenticated:
        messages.warning(request, 'You are already registered!')
        return redirect('vendordashboard')
    elif request.method =='POST':
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
            user.role = User.VENDOR
            user.save()
            vendor = vendor_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()

            send_verification_email(request, user)
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

def activate_user(request,uidb64, token):
    return
def login (request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged-in.')
        return redirect('myaccount')
    elif request.method =='POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You have been logged-in.')
            return redirect('myaccount')
        else:
            messages.error(request, 'Invalid login credentials.')
            return redirect('login')
    return render (request, 'accounts/login.html')

def logout (request):
    auth.logout(request)
    messages.info(request,'You are now logged-out.')
    return redirect ('login')

@login_required(login_url='login')
def myaccount(request):
    user = request.user
    redirecturl = detectuser(user)
    return redirect(redirecturl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customerdashboard (request):
    return render (request, 'accounts/customerdashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendordashboard (request):
    return render (request, 'accounts/vendordashboard.html')

