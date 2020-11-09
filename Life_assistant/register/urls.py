from django.urls import path
from . import views

urlpatterns = [
    # 127.0.0.1:8000/register/index
    path('index',views.index_view),
    path('register',views.register_view),
    path('send_email',views.send_view)
]