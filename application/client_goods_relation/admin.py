from django.contrib import admin

from client_goods_relation.models import Comment, Like, InFavorites

# Register your models here.
admin.site.register(Like)
admin.site.register(InFavorites)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('owner', 'goods')
