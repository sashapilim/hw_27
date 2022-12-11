from django.db import models

# Create your models here.
class Categories(models.Model):
    name = models.CharField(max_length=50, unique=True)

#id,name,author,price,description,address,is_published

class Ads(models.Model):
    name = models.CharField(max_length=250)
    author = models.CharField(max_length=50)
    price= models.PositiveSmallIntegerField()
    description = models.CharField(max_length=250)
    address = models.CharField(max_length=100)
    is_published=models.BooleanField()
