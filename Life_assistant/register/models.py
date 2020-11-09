from django.db import models


# Create your models here.
class User_mian(models.Model):
    username = models.CharField('用户名', max_length=11)
    nickname = models.CharField("昵称", max_length=50)
    email = models.EmailField('邮箱')
    password = models.CharField('密码', max_length=32)

    class Meta:
        # 表名
        db_table = 'user_info'
        # 子页面（单数）名称
        verbose_name= '用户名或邮箱'
        # admin界面中显示名称（复数）
        verbose_name_plural='用户信息'

