from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^main$', views.main),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^travels$', views.dashboard),
    url(r'^travels/destination/(?P<id>\d+)$', views.destination),
    url(r'^travels/join/(?P<id>\d+)$', views.join),
    url(r'^travels/add$', views.add),
    url(r'^addnew$', views.addnew),
    url(r'^logout$', views.logout)
]