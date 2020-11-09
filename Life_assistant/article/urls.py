from django.urls import path
from . import views

# app_name = 'article'
urlpatterns = [
    # path函数将url映射到视图
    # 127.0.0.1:8000/article/artlist
    path('artlist', views.article_list),

    # 127.0.0.1:8000/article/article_detail
    path('article_detail/<int:id>', views.article_detail),

    # 删除
    path('article_delete/<int:id>', views.article_delete),
    # 编辑判断
    path('edit/<int:id>', views.edit),
    # 进行编辑页面
    path('update/<int:id>', views.update),

    # 发帖
    path('log_dec', views.log_dec),
    # path('create',views.create),
    path('create/<str:username>', views.create),
    # 热门排序
    path('total_views', views.total_views),

]
