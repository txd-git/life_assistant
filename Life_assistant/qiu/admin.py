from django.contrib import admin

# Register your models here.
from .models import History
class HistoryManage(admin.ModelAdmin):
    list_display = ['id', 'nper', 'time']
    # 后台界面显示什么
    list_display_links = ['nper', 'time']
    # 查询界面可以显示那个字段
    list_filter = ['nper', 'time']
    # 过滤器


# 要自定义管理类与模型类关联
admin.site.register(History, HistoryManage)