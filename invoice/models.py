from django.db import models


# Create your models here.

class Manufacturer(models.Model):
    manufacturer_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.manufacturer_name


class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = 'Categories'


class Device(models.Model):
    device_name = models.CharField(max_length=200, unique=True)
    device_description = models.TextField(null=True)
    device_manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, null=True)
    device_category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.device_name
