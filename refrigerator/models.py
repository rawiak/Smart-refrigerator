from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from .validators import valid_range


class Category(models.Model):
    category_name = models.CharField(max_length = 64)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    name = models.CharField(max_length=64, verbose_name='Nazwa')
    description = models.TextField()
    quantity = models.IntegerField(verbose_name='Ilość', validators=[valid_range])
    expiration_date = models.DateField(verbose_name='Data ważności')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Kategoria:')

    def __str__(self):
        return '{}-{}/ data ważności:{}'.format(self.name,self.category, self.expiration_date)
