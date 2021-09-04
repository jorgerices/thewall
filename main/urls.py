from django.urls import path
from . import views, auth

urlpatterns = [
    path('', views.index),
    path('signin', auth.signin),
    path('login', auth.login),
    path('logout', auth.logout),
    path('home', views.home)
]