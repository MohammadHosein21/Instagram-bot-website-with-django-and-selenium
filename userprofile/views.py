from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from .models import UserProfile
from Bot import Bot


# Create your views here.

@login_required
def profile(request):
    if request.method == 'POST':
        if request.POST['username'] and request.POST['password']:
            userprofile = UserProfile()
            userprofile.user = request.user
            userprofile.usernameIG = request.POST['username']
            userprofile.passwordIG = request.POST['password']
            userprofile.save()
            return redirect('profile_detail')
        else:
            return render(request, 'profile.html', {'error': 'All fields is required'})
    else:
        return render(request, 'profile.html')


@login_required
def profiledetail(request):
    id = request.user.id
    name = request.user.username
    try:
        userdetail = UserProfile.objects.values_list('usernameIG', 'passwordIG')
        pagedetail = userdetail.filter(pk=id)
        return render(request, 'profile_detail.html', {'pagedetail': pagedetail, 'id': id, 'name': name})
    except AttributeError:
        return render(request, 'profile_detail.html', {'error': 'You dont have any pages!!!', 'id': id, 'name': name})


@login_required
def startbot(request):
    id = request.user.id
    userdetail = UserProfile.objects.values_list('usernameIG', 'passwordIG')
    pagedetail = userdetail.filter(pk=id)
    detail_list = []
    for detail in pagedetail:
        detail_list = list(detail)
    bot = Bot()
    bot.login()
    bot.enterUsernamePassword(username_input=detail_list[0], password_input=detail_list[1])
    bot.likePhoto(request.POST['tag'], int(request.POST['count']))
    return render(request, 'startbot.html', {'u': detail_list})
