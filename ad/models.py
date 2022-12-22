from django.db import models


# Create your models here.
class Categories(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


# iid,first_name,last_name,username,password,role,age,location_id

#
class Ads(models.Model):
    name = models.CharField(max_length=250)
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    price = models.PositiveSmallIntegerField()
    description = models.CharField(max_length=500)

    is_published = models.BooleanField()
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    image = models.ImageField(null=True, upload_to='pictures', blank=True)


    class Meta:
        verbose_name = "Обьявление"
        verbose_name_plural="Обьявления"

    def __str__(self):
        return self.name