from django.contrib import admin

# Register your models here.

from django.contrib import admin

# 别忘了导入ArticlerPost
from .models import ArticlePost

# 注册ArticlePost到admin中
class ArticlePostManage(admin.ModelAdmin):
    list_display = ['id', 'title', 'created']
    # 后台界面显示什么
    list_display_links = ['title']
    # 可以根据哪些字段查询
    search_fields = ['title', 'created']
    # 设置启用Admin 更改列表页面上的搜索框。
    list_filter = ['title',]
    # 过滤器
# 要自定义管理类与模型类关联
admin.site.register(ArticlePost, ArticlePostManage)
