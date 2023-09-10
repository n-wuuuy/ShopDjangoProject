from django.conf import settings
from django.db import models

from goods.models import Goods


class Like(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.owner.username}: Book {self.goods.name}'


class Comment(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              blank=True, related_name='owner_comment')
    text = models.TextField()
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name='comment')


class InFavorites(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)
    favorite = models.BooleanField(default=False)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)


class Basket(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
