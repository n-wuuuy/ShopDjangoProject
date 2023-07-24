from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class GoodsSize(models.Model):
    size_name = models.CharField(max_length=50)
    size_value = models.DecimalField(max_digits=6, decimal_places=2, null=True, default=None)

    def __str__(self):
        return f'{self.size_name} {self.size_value}'


class GoodsCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(f'{self.name}')


class Goods(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    images = models.ImageField(upload_to=f'photo/')
    size = models.ManyToManyField(GoodsSize)
    discount = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])
    time_create = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(GoodsCategory, on_delete=models.PROTECT)
    is_published = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255, default=owner.name)

    class Meta:
        ordering = ['-time_create']

    def __str__(self):
        return f'{self.name} :{self.price}'

    def get_absolute_url(self):
        return reverse(self.category.name, kwargs={'goods_slug': self.slug})
