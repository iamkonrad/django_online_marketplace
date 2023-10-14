from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User



def registeruser(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 2
            user.save()
            return redirect('registeruser')
    else:
        form = UserForm()
    context = {
        'form':form,
    }
    return render(request, 'accounts/registeruser.html', context)
