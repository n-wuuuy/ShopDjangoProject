from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class GoodsSize(models.Model):
    size_name = models.CharField(max_length=50)
    size_value = models.DecimalField(max_digits=6, decimal_places=2, null=True, default=None, blank=True)

    def __str__(self):
        return f'{self.size_name} {self.size_value}'


class GoodsCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(f'{self.name}')


class Goods(models.Model):
    def file_name(instance, filename):
        return '/'.join(['images', str(instance.name), filename])

    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to=file_name, blank=True, null=True)
    size = models.ManyToManyField(GoodsSize, related_name='size_goods')
    discount = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])
    time_create = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(GoodsCategory, on_delete=models.PROTECT, related_name='category_goods')
    is_published = models.BooleanField(default=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)
    company_name = models.CharField(max_length=255)

    class Meta:
        ordering = ['-time_create']

    def __str__(self):
        return f'{self.name} :{self.price}'

    def get_absolute_url(self):
        return reverse('goods_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class GoodsImages(models.Model):
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to=f'photo/')
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name='goods_images')

    def __str__(self):
        return self.title


class Comment(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              blank=True, related_name='owner_comment')
    text = models.TextField()
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name='comment')
