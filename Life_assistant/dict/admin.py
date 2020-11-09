from django.contrib import admin

# Register your models here.
from .models import Words


class WordsManage(admin.ModelAdmin):
    list_display = ['id', 'word', 'mean']
    # 后台界面显示什么
    list_display_links = ['id', 'word']
    # 可以根据哪些字段查询


# 要自定义管理类与模型类关联
admin.site.register(Words, WordsManage)
