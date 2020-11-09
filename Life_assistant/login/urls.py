from django.urls import path
from . import views
urlpatterns = [
    # 127.0.0.1:8000/login/index
    path('index',views.index_view),
    path('loging',views.loging_view),
    path('home_page',views.home_page_view),
    path('validation_state',views.validation_state_view)
]