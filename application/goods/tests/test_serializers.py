from django.contrib.auth.models import User
from django.db.models import Count, Case, F, When
from django.test import TestCase

from client_goods_relation.models import ClientGoodsRelation
from goods.models import Goods, GoodsSize, GoodsCategory
from goods.serializers import GoodsSerializer


class GoodsSerializerTestCase(TestCase):
    def test_performance(self):
        user1 = User.objects.create(username='user1',
                                    first_name='Ivan',
                                    last_name='Danilevich')
        user2 = User.objects.create(username='user2',
                                    first_name='Ivan',
                                    last_name='Sidorov')
        user3 = User.objects.create(username='user3',
                                    first_name='1',
                                    last_name='2')
        goods_size1 = GoodsSize.objects.create(size_name='EU', size_value=26.00)
        goods_size2 = GoodsSize.objects.create(size_name='XL', size_value=1.00)
        goods_category1 = GoodsCategory.objects.create(name='Shoes', slug='shoes')
        goods_category2 = GoodsCategory.objects.create(name='Clothe', slug='clothe')
        goods1 = Goods.objects.create(name='New Balance',
                                      slug='new_balance',
                                      description='cool shoes',
                                      price=250.00,
                                      images=f'photo/shoes2.jpg',
                                      category=goods_category1,
                                      owner=user1,
                                      company_name='New Balance')
        goods1.size.set([goods_size1.pk])
        goods2 = Goods.objects.create(name='Nike Hudi',
                                      slug='nike_hudi',
                                      description='cool cloth',
                                      price=150.00,
                                      images=f'photo/Clothe.jpg',
                                      category=goods_category2,
                                      owner=user2,
                                      company_name='Nike')
        goods2.size.set([goods_size1.pk, goods_size2.pk])
        ClientGoodsRelation.objects.create(user=user2, goods=goods1, like=True)
        ClientGoodsRelation.objects.create(user=user1, goods=goods1, like=True)
        ClientGoodsRelation.objects.create(user=user3, goods=goods2, like=True)
        ClientGoodsRelation.objects.create(user=user2, goods=goods2, like=False)
        goods = Goods.objects.all().annotate(likes=Count(Case(When(clientgoodsrelation__like=True, then=1))),
                                             owner_name=F('owner__username'),
                                             price_with_discount=(F('price') -
                                                                  F('price') *
                                                                  F('discount') / 100),
                                             category_name=F('category__name')
                                             ).order_by('time_create')
        data = GoodsSerializer(goods, many=True).data
        exected_data = [
            {
                'name': 'New Balance',
                'price_with_discount': '250.00',
                'images': '/media/photo/shoes2.jpg',
                'id': goods1.id,
                'likes': 2,
                'owner_name': 'user1',
                'is_published': True,
                'category_name': 'Shoes',
                'company_name': 'New Balance',
                'time_create': goods1.time_create.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            },
            {
                'name': 'Nike Hudi',
                'price_with_discount': '150.00',
                'images': '/media/photo/Clothe.jpg',
                'id': goods2.id,
                'likes': 1,
                'owner_name': 'user2',
                'is_published': True,
                'category_name': 'Clothe',
                'company_name': 'Nike',
                'time_create': goods2.time_create.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            }
        ]
        self.assertEquals(exected_data, data)
