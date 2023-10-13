from django.shortcuts import render



def registerUser(request):
    return render(request, 'accounts/registerUser.html')
