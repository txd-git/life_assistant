from django.db import models

# Create your models here.
class History(models.Model):
    nper = models.CharField('期号',max_length=20)
    red_one = models.CharField('红1',max_length=10)
    red_two = models.CharField('红2',max_length=10)
    red_three = models.CharField('红3',max_length=10)
    red_four = models.CharField('红4',max_length=10)
    red_five = models.CharField('红5',max_length=10)
    red_six = models.CharField('红6',max_length=10)
    blue = models.CharField('蓝球',max_length=10)
    time = models.CharField('开奖日期',max_length=20)

    class Meta:
        db_table='history'
        # 子页面（单数）名称
        verbose_name='开奖期号'
        # admin界面中显示名称（复数）
        verbose_name_plural='双色球开奖记录'