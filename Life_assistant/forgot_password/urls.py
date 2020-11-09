from django.urls import path
from . import views
urlpatterns = [
    # 127.0.0.1:8000/forgot_password/index
    path('index',views.forgot_password_view),
    path('email_validation',views.email_validation_view),
    path('send_validation',views.send_validation_view)
]