from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode

from vendor.forms import VendorForm
from vendor.models import Vendor
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

            mail_subject = 'Please activate your account'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request,user, mail_subject, email_template)                                         #Verification email
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

            mail_subject = 'Please activate your account'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request,user, mail_subject, email_template)                                         #Verification email
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
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account is now active.')
        return redirect('myaccount')
    else:
        messages.error(request,'Invalid activation link.')
        return redirect('myaccount')

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
    vendor = Vendor.objects.get(user=request.user)
    context = {
        'vendor':vendor,
    }

    return render (request, 'accounts/vendordashboard.html', context)

def forgot_password(request):
    if request.method =='POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            mail_subject = 'Password reset'
            email_template = 'accounts/emails/reset_password_email.html'
            send_verification_email(request,user, mail_subject, email_template)

            messages.success(request, 'Reset link has been sent to you.')
            return redirect('login')
        else:
            messages.error(request, 'Account not found.')
            return redirect('forgot_password')

    return render(request, 'accounts/forgot_password.html')

def reset_password_validate(request,uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.info(request, 'Please reset your password')
        return redirect('reset_password')


def reset_password(request):
    if request.method =='POST':
        password = request.POST['password']
        confirm_password = request.POST['password']

        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password has been reset.')
        else:
            messages.error(request,'Passwords do not match')
            return redirect('login')

    return render(request, 'accounts/reset_password.html')
