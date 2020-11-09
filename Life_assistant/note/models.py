from django.db import models
from register.models import User_mian


# Create your models here.
class Note(models.Model):
    title = models.CharField('标题', max_length=100)
    content = models.TextField('内容')
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    updated_time = models.DateTimeField('更新时间', auto_now=True)
    is_active = models.BooleanField('是否活跃', default=True)
    user = models.ForeignKey(User_mian, on_delete=models.CASCADE)

    class Meta:
        # 表名
        db_table = 'note'
        # 按创建时间降排列
        ordering = ('-created_time',)
        # 子页面（单数）名称
        verbose_name = '日记标题'
        # admin界面中显示名称（复数）
        verbose_name_plural = '用户日记'
