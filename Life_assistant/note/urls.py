from django.urls import path
from . import views

urlpatterns = [
    path('page_add_note', views.page_add_note), # 添加日记页面路由
    path('add_note', views.add_note_view),  # 添加日记数据处理路由

    path('page_update_note/<int:nid>',views.page_update_note),   # 修改日记页面路由
    path('update_note', views.update_note_view),  # 修改日记数据处理路由

    path('all_notes', views.all_notes),
    # 日记页面路由
    path('all_note', views.all_note_view),  # 日记列表路由

    path('delete_note/<int:nid>', views.delete_note_view),  # 删除日记路由

    path('one_note/<int:nid>',views.one_note_view), # 一篇日记的路由

    # 给前段页面日期路由
    # path('send_data',views.send_data_view),
]
