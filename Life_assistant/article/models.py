from register.models import User_mian
from django.db import models
from django.utils import timezone

# timezone 用于处理时间相关事务。


# 博客文章数据模型
class ArticlePost(models.Model):
    title = models.CharField('标题', max_length=100)
    body = models.TextField('正文')
    created = models.DateTimeField('创建时间',default=timezone.now)
    updated = models.DateTimeField('更新时间',auto_now=True)
    total_views = models.PositiveIntegerField('浏览量',default=0)
    author = models.ForeignKey(User_mian, on_delete=models.CASCADE)

    class Meta:
        # 表名
        db_table = "article"
        # 按创建时间降排列
        ordering = ('-created',)
        # 子页面（单数）名称
        verbose_name='论坛标题'
        # admin界面中显示名称（复数）
        verbose_name_plural='吐槽论坛'

