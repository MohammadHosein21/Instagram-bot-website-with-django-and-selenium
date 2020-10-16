from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from .models import UserProfile


# Create your views here.
# def profile(request):
#     return render(request, 'profile.html')

@login_required
def profile(request):
    if request.method == 'POST':
        if request.POST['username'] and request.POST['password']:
            userprofile = UserProfile()
            userprofile.user_id = request.user.pk
            userprofile.usernameIG = request.POST['username']
            userprofile.passwordIG = request.POST['password']
            userprofile.save()
            return redirect('home')
        else:
            return render(request, 'profile.html', {'error': 'All fields are require'})
    else:
        return render(request, 'profile.html')
