from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$',views.index),
    url(r'^register',views.register),
    url(r'^quotes$',views.quotes),
    url(r'^quotes/addquote',views.addQuote),
    url(r'^quotes/(?P<id>\d+)/like$',views.likeQuote),
    url(r'^quotes/(?P<id>\d+)/delete$',views.deleteQuote),
    url(r'^myaccount/(?P<id>\d+)$', views.myAccount),
    url(r'^user/(?P<id>\d+)$', views.displayUser),
    url(r'^user/(?P<id>\d+)/update$', views.updateUser),
    url(r'^login',views.login),
    url(r'^logout',views.logout)
]