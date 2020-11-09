from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('index',views.speech),
    path('callback',views.callback),
]
