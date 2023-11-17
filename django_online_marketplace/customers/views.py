from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from accounts.forms import UserProfileForm, UserInfoForm
from accounts.models import UserProfile


@login_required(login_url='login')
def customer_profile(request):
    profile = get_object_or_404(UserProfile, user = request.user)
    profile_form = UserProfileForm(instance = profile)
    user_form = UserInfoForm(instance = request.user)

    context = {
        'profile_form':profile_form,
        'user_form':user_form,
    }

    return render(request, 'customers/customer_profile.html', context)
