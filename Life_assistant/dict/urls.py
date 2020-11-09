from django.urls import path
from . import views

urlpatterns = [
    path('check_word',views.check_word),
    path('check_word_server',views.check_word_server),
]