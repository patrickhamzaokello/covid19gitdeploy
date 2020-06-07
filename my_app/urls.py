from django.contrib.auth import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.basepage, name='home'),
    path('globaldata/', views.globaldata, name='globaldata'),
    path('cov19Info/', views.wikipage, name='wikipage'),
    path('about/', views.aboutpage, name='aboutpage'),
    path('news/', views.newspage, name='newspage'),


]