from django.contrib import admin

from goods.models import Goods, GoodsSize, GoodsCategory


class GoodsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class GoodsCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Goods, GoodsAdmin)
admin.site.register(GoodsSize)
admin.site.register(GoodsCategory, GoodsCategoryAdmin)
