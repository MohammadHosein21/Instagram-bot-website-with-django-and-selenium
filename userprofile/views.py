import datetime
import numpy as np
from rest_framework.response import Response
from rest_framework.views import APIView
from scipy.ndimage.interpolation import shift
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from selenium.common.exceptions import NoSuchElementException
import schedule
from .models import UserProfile, Data
from Bot import Bot
from time import sleep
from django.http import JsonResponse


# Create your views here.
#
    # def getData(request):
    #     labels = ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange']
    #     data = {
    #         "labels": labels,
    #     }
    #     return JsonResponse(data)


# class ChartData(APIView):
#     authentication_classes = []
#     permission_classes = []
#     def get(self, request, format=None):
#         qs_count = User.objects.all().count()
#         labels = ['Users', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange']
#         default_items = [qs_count,23,2,2,25,23,3]
#         data = {
#             'labels' : labels,
#             'default' : default_items
#         }
#         return Response(data)

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
        followerList = Data.objects.values_list('follower').filter(pk=id)[0][0]
        dateList = Data.objects.values_list('date').filter(pk=id)[0][0]
        dateStr = []
        for i in range(len(dateList)):
            dateStr.append( dateList[i].strftime("%d-%b-%Y"))
        return render(request, 'userprofile/templates/pagedetail.html',
                      {'pagedetail': pagedetail, 'name': name, 'follower': followerList, 'date': dateStr})
    except AttributeError:
        return render(request, 'userprofile/templates/pagedetail.html',
                      {'error': 'You dont have any pages!!!', 'id': id, 'name': name, })


@login_required
def startbot(request):
    def taskFollow():
        id = request.user.id
        userdetail = UserProfile.objects.values_list('usernameIG', 'passwordIG')
        pagedetail = userdetail.filter(pk=id)
        detail_list = []
        for detail in pagedetail:
            detail_list = list(detail)
        bot = Bot()
        bot.login()
        bot.enterUsernamePassword(username_input=detail_list[0], password_input=detail_list[1])
        bot.followOtherpage(request.POST['tag'])
        return render(request, 'startbot.html')

    def taskPostComment():
        id = request.user.id
        userdetail = UserProfile.objects.values_list('usernameIG', 'passwordIG')
        pagedetail = userdetail.filter(pk=id)
        detail_list = []
        for detail in pagedetail:
            detail_list = list(detail)
        bot = Bot()
        bot.login()
        bot.enterUsernamePassword(username_input=detail_list[0], password_input=detail_list[1])
        bot.postComment(request.POST['tag'], request.POST['comment'])
        return render(request, 'startbot.html')

    def taskLike():
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
        return render(request, 'startbot.html', )

    def taskUnfollow():
        id = request.user.id
        userdetail = UserProfile.objects.values_list('usernameIG', 'passwordIG')
        pagedetail = userdetail.filter(pk=id)
        detail_list = []
        for detail in pagedetail:
            detail_list = list(detail)
        bot = Bot()
        bot.login()
        bot.enterUsernamePassword(username_input=detail_list[0], password_input=detail_list[1])
        bot.unfollow(page_id=detail_list[0])
        return render(request, 'startbot.html', )

    def taskGetFollowersNumber():
        id = request.user.id
        userdetail = UserProfile.objects.values_list('usernameIG', 'passwordIG')
        pagedetail = userdetail.filter(pk=id)
        detail_list = []
        for detail in pagedetail:
            detail_list = list(detail)
        bot = Bot()
        bot.login()
        bot.enterUsernamePassword(username_input=detail_list[0], password_input=detail_list[1])
        follower = bot.getFollowersNumber(page_id=detail_list[0])
        date = datetime.datetime.now()
        followerList = Data.objects.values_list('follower').filter(pk=id)[0][0]
        dateList = Data.objects.values_list('date').filter(pk=id)[0][0]
        if len(followerList) < 30:
            followerList.append(follower)
        else:
            for i in range(len(followerList) - 1):
                followerList[i] = followerList[i + 1]
            followerList[len(followerList) - 1] = follower
        if len(dateList) < 30:
            dateList.append(date)
        else:
            for i in range(len(dateList) - 1):
                dateList[i] = dateList[i + 1]
            dateList[len(dateList) - 1] = date
        data = Data()
        userprofile = UserProfile()
        userprofile.user = request.user
        data.user = request.user
        data.follower = followerList
        data.date = dateList
        userprofile.followers = follower
        userprofile.usernameIG = detail_list[0]
        userprofile.passwordIG = detail_list[1]
        userprofile.save()
        data.save()
        return render(request, 'userprofile/templates/startbot.html', {'follower': follower})

    schedule.every(2).hours.do(taskFollow)
    schedule.every().day.do(taskPostComment)
    schedule.every(2).hours.do(taskLike)
    schedule.every().friday.at("23:00").do(taskUnfollow)
    schedule.every().day.at("23:55").do(taskGetFollowersNumber)

    while True:
        schedule.run_pending()
        sleep(1)
