from django.contrib import admin

from client_goods_relation.models import Comment, Like

# Register your models here.
admin.site.register(Like)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('owner', 'goods')
