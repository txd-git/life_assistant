from django.db import models


# Create your models here.
class City(models.Model):
    """城市即对应 """
    city_name = models.CharField('地区名称',max_length=10,default='')
    number = models.CharField('地区编号',max_length=20,default=0)

    class Meta:
        # 表名
        db_table='city'
        # 子页面（单数）名称
        verbose_name='城市名称'
        # admin界面中显示名称（复数）
        verbose_name_plural='天气对应城市编号'
