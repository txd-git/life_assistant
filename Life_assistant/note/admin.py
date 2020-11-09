from django.contrib import admin

# Register your models here.
from .models import Note


class NoteManage(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'updated_time']
    # 后台界面显示什么
    list_display_links = ['title']
    # 可以根据哪些字段查询


# 要自定义管理类与模型类关联
admin.site.register(Note, NoteManage)
