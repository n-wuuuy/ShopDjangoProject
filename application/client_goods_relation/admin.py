from django.contrib import admin

from client_goods_relation.models import Comment, Like, InFavorites, Basket

# Register your models here.
admin.site.register(Like)
admin.site.register(InFavorites)
admin.site.register(Basket)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('owner', 'goods')
