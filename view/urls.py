from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    
    url(r'^$',views.index),
    path('getHistory/', views.getHistory,name='getHistory'),
    path('getOnlineRecords/', views.getOnlineRecords,name='getOnlineRecords'),
    path('technical/', views.technical,name='technical'),

    ]