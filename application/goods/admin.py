from django.contrib import admin
from django.utils.safestring import mark_safe

from goods.models import Goods, GoodsSize, GoodsCategory, GoodsImages


class GoodsImagesInline(admin.TabularInline):
    model = GoodsImages
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="110"')

@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'category', 'owner', 'company_name', 'id', 'is_published', 'get_image')
    list_filter = ('time_create', 'category', 'is_published')
    search_fields = ('name', 'category__name', 'company_name', 'owner__username')
    save_on_top = True
    list_editable = ('is_published',)
    inlines = [GoodsImagesInline]
    readonly_fields = ("get_image",)
    fieldsets = (
        (None, {
            "fields": (("name", "slug"),)
        }),
        (None, {
            "fields": (("price", "discount"),)
        }),
        (None, {
            "fields": (("owner", "company_name",),)
        }),
        (None, {
            "fields": (("category", "size"),)
        }),
        (None, {
            "fields": (("image", "get_image"),)
        })
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="110"')

    get_image.short_description = 'Photo'


@admin.register(GoodsCategory)
class GoodsCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(GoodsImages)
class GoodsImagesAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'goods', 'get_image')

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="110"')


admin.site.register(GoodsSize)
