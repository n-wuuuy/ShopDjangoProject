from django import template

from goods.models import GoodsCategory

register = template.Library()


@register.simple_tag()
def get_category():
    return GoodsCategory.objects.all()
