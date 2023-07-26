from django.contrib.auth.models import User
from django.db.models import F, Count, Case, When
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from client_goods_relation.models import ClientGoodsRelation
from goods.models import GoodsSize, GoodsCategory, Goods
from goods.serializers import GoodsSerializer


class GoodsApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='user1',
                                        first_name='Ivan',
                                        last_name='Danilevich')
        goods_size1 = GoodsSize.objects.create(size_name='EU', size_value=26.00)
        goods_size2 = GoodsSize.objects.create(size_name='XL', size_value=1.00)
        goods_category1 = GoodsCategory.objects.create(name='Shoes', slug='shoes')
        goods_category2 = GoodsCategory.objects.create(name='Clothe', slug='clothe')
        self.goods_1 = Goods.objects.create(name='New Balance',
                                            slug='new_balance',
                                            description='cool shoes',
                                            price=250.00,
                                            images=f'photo/shoes2.jpg',
                                            category=goods_category1,
                                            owner=self.user,
                                            company_name='New Balance')
        self.goods_1.size.set([goods_size1.pk])
        self.goods_2 = Goods.objects.create(name='Nike Hudi',
                                            slug='nike_hudi',
                                            description='cool cloth',
                                            price=150.00,
                                            images=f'photo/Clothe.jpg',
                                            category=goods_category2,
                                            owner=self.user,
                                            company_name='Nike')
        self.goods_2.size.set([goods_size1.pk, goods_size2.pk])
        self.goods_3 = Goods.objects.create(name='Nike Jornad',
                                            slug='nike_jornad',
                                            description='cool shoes',
                                            price=150.00,
                                            images=f'photo/shoes3.jpg',
                                            category=goods_category1,
                                            owner=self.user,
                                            company_name='Nike')
        self.goods_3.size.set([goods_size1.pk, goods_size2.pk])
        ClientGoodsRelation.objects.create(user=self.user, goods=self.goods_1, like=True)

    def test_get(self):
        url = reverse('goods-list')
        response = self.client.get(url)
        for objects in response.data:
            objects['images'] = objects['images'][17:]
        goods = Goods.objects.all().annotate(
            likes=Count(Case(When(clientgoodsrelation__like=True, then=1))),
            owner_name=F('owner__username'),
            price_with_discount=(F('price') -
                                 F('price') *
                                 F('discount') / 100),
            category_name=F('category__name')
        ).order_by('time_create')
        serializer_data = GoodsSerializer(goods, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(serializer_data[0]['likes'], 1)

    def test_get_search(self):
        url = reverse('goods-list')
        response = self.client.get(url,  data={'search': 'Nike'})
        for objects in response.data:
            objects['images'] = objects['images'][17:]
        goods = Goods.objects.filter(id__in=[self.goods_2.id, self.goods_3.id]).annotate(
            likes=Count(Case(When(clientgoodsrelation__like=True, then=1))),
            owner_name=F('owner__username'),
            price_with_discount=(F('price') -
                                 F('price') *
                                 F('discount') / 100),
            category_name=F('category__name')
        ).order_by('time_create')
        serializer_data = GoodsSerializer(goods, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_sort(self):
        url = reverse('goods-list')
        response = self.client.get(url, data={'ordering': 'price_with_discount'})
        for objects in response.data:
            objects['images'] = objects['images'][17:]
        goods = Goods.objects.all().annotate(
            likes=Count(Case(When(clientgoodsrelation__like=True, then=1))),
            owner_name=F('owner__username'),
            price_with_discount=(F('price') -
                                 F('price') *
                                 F('discount') / 100),
            category_name=F('category__name')
        ).order_by('price_with_discount')
        serializer_data = GoodsSerializer(goods, many=True).data
        print(serializer_data)
        print(response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
