from django.contrib import admin
from store.models import Product, Collection, ProductColor, ProductImage, AboutImage, About, OurAdvantage, News, Slyder, \
    PublicOffer, Help, ImageHelp, Color


class ImageAdminInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    max_num = 8


class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageAdminInline]


class CollectionAdmin(admin.ModelAdmin):
    pass


class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'rgb']


class ProductColorAdmin(admin.ModelAdmin):
    list_display = ['image', 'color']


class AboutImageAdminInline(admin.TabularInline):
    model = AboutImage
    extra = 0
    max_num = 3


class AboutAdmin(admin.ModelAdmin):
    inlines = [AboutImageAdminInline]


class AboutImageAdmin(admin.ModelAdmin):
    list_display = ['page', 'image']


class OurAdvantageAdmin(admin.ModelAdmin):
    list_display = ['headline', 'description', 'icon']


class NewsAdmin(admin.ModelAdmin):
    list_display = ['headline', 'description', 'photo']


class SlyderAdmin(admin.ModelAdmin):
    list_display = ['photo', 'link']


class PublicOfferAdmin(admin.ModelAdmin):
    list_display = ['headline', 'description']


class HelpAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer']


class ImageHelpAdmin(admin.ModelAdmin):
    list_display = ['image', 'page']


admin.site.register(Product, ProductAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(ProductColor, ProductColorAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(About, AboutAdmin)
admin.site.register(OurAdvantage, OurAdvantageAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Slyder, SlyderAdmin)
admin.site.register(PublicOffer, PublicOfferAdmin)
admin.site.register(Help, HelpAdmin)
admin.site.register(ImageHelp, ImageHelpAdmin)


