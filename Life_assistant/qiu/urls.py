from django.urls import path
from . import views
urlpatterns = [
    # 127.0.0.1:8000/qiu/index
    path('index',views.index),
    path('generate',views.generate),
    path('query',views.query),
]