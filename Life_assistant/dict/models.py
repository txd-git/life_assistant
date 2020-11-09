from django.db import models


# Create your models here.
class Words(models.Model):
    word = models.CharField('单词', max_length=50)
    mean = models.CharField('解释', max_length=500)

    class Meta:
        # 表名
        db_table = 'word'
        # 子页面（单数）名称
        verbose_name = '单词'
        # admin界面中显示名称（复数）
        verbose_name_plural = '单词翻译'
