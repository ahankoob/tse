from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    
    url(r'^$',views.index),
    url(r'^getJson/',views.symbolsJson,name='symbolsJson'),
    url(r'^CheckActive/',views.symbolsCheckActive,name='symbolsCheckActive'),
    path('getHistory/<int:sid>/', views.getHistory,name='getHistory'),
    path('importFastData/<int:sid>/', views.importFastData,name='importFastData'),
    path('technical/<int:sid>/', views.myTechnical,name='myTechnical'),
    path('getsymbols/', views.tickersFromTseSite,name='tickersFromTseSite'),

    ]