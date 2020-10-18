from django.conf.urls import url

from . import views

urlpatterns = [
    
    url(r'^$',views.index),
    url(r'^getHistory/(?P<sid>[0-9]+)/',views.getHistory,name='getHistory'),
    
    ]