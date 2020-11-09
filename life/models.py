from django.db import models


# Create your models here.
class City(models.Model):
    city_name = models.CharField(max_length=20)
    numble = models.CharField(max_length=20)
