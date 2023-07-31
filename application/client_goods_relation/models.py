from django.conf import settings
from django.db import models


from goods.models import Goods


class ClientGoodsRelation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}: Book {self.goods.name}'
