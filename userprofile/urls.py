from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.InsertPage, name='profile'),
    path('details', views.pageDetails, name='profile_detail'),
    path('startbot', views.startbot, name='startbot'),
    # path('chart/data',views.getData,name = 'chartData'),
]
