from django.urls import path
from . import views

urlpatterns = [
    # 127.0.0.1:8000/tq/index
    path('index', views.index),
    path('get_addree',views.get_addree),
    path('get_weather', views.get_weather),
]
