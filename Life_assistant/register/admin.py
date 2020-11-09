from django.contrib import admin

# Register your models here.
from .models import User_mian
class User_mianManage(admin.ModelAdmin):
    list_display = ['id', 'username', 'email']
    # 后台界面显示什么
    list_display_links = ['id']
    # 可以根据哪些字段查询
    search_fields = ['username', 'email']
    # 设置启用Admin 更改列表页面上的搜索框。
    list_editable = ['username', 'email']
    # 查询界面可以显示那个字段
    list_filter = ['username', 'email']
    # 过滤器


# 要自定义管理类与模型类关联
admin.site.register(User_mian, User_mianManage)