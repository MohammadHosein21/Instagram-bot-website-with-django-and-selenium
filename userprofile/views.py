from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from selenium.common.exceptions import NoSuchElementException

from .models import UserProfile
from Bot import Bot


# Create your views here.

@login_required
def InsertPage(request):
    if request.method == 'POST':
        try:
            if request.POST['username'] and request.POST['password']:
                userprofile = UserProfile()
                userprofile.user = request.user
                userprofile.usernameIG = request.POST['username']
                userprofile.passwordIG = request.POST['password']
                bot = Bot()
                bot.login()
                bot.enterUsernamePassword(username_input=request.POST['username'],
                                          password_input=request.POST['password'])
                userprofile.followers = bot.getFollowersNumber(page_id=request.POST['username'])
                userprofile.save()
                return redirect('profile_detail')
            else:
                return render(request, 'userprofile/templates/insertpage.html', {'error': 'All fields is required'})
        except NoSuchElementException:
            return render(request, 'userprofile/templates/insertpage.html',
                          {'error': 'Username or Password is incorrect !!!'})

    else:
        return render(request, 'userprofile/templates/insertpage.html')


@login_required
def pageDetails(request):
    id = request.user.id
    name = request.user.username
    try:
        userdetail = UserProfile.objects.values_list('usernameIG', 'passwordIG', 'followers')
        pagedetail = userdetail.filter(pk=id)
        # detail_list = []
        # for detail in pagedetail:
        #     detail_list = list(detail)
        # if detail_list == []:
        #     return render(request, 'userprofile/templates/pagedetail.html',
        #                   {'error': 'You dont have any pages!!!', 'id': id, 'name': name})
        # else:
        #     bot = Bot()
        #     bot.login()
        #     bot.enterUsernamePassword(username_input=detail_list[0], password_input=detail_list[1])
        #     follower = bot.getFollowersNumber(page_id=detail_list[0])
        return render(request, 'userprofile/templates/pagedetail.html',
                      {'pagedetail': pagedetail, 'name': name})
    except AttributeError:
        return render(request, 'userprofile/templates/pagedetail.html',
                      {'error': 'You dont have any pages!!!', 'id': id, 'name': name})


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
    # bot.likePhoto(request.POST['tag'], int(request.POST['count']))
    bot.followOtherpage(request.POST['tag'],int(request.POST['amount']))
    return render(request, 'startbot.html', {'u': detail_list})
