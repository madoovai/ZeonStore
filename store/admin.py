from django.contrib import admin
from store.models import Product, Collection, ProductImage, AboutImage, About, OurAdvantage, News, \
    PublicOffer, Help, ImageHelp, Color, Slider, Bag


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


class AboutImageAdminInline(admin.TabularInline):
    model = AboutImage
    extra = 0
    max_num = 3


class BagAdmin(admin.ModelAdmin):
    list_display = ['product_id', 'amount_of_product']


class AboutAdmin(admin.ModelAdmin):
    inlines = [AboutImageAdminInline]


class AboutImageAdmin(admin.ModelAdmin):
    list_display = ['page', 'image']


class OurAdvantageAdmin(admin.ModelAdmin):
    list_display = ['headline', 'description', 'icon']


class NewsAdmin(admin.ModelAdmin):
    list_display = ['headline', 'description', 'photo']


class SliderAdmin(admin.ModelAdmin):
    list_display = ['photo', 'link']


class PublicOfferAdmin(admin.ModelAdmin):
    list_display = ['headline', 'description']


class HelpAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer']


class ImageHelpAdmin(admin.ModelAdmin):
    list_display = ['image']


admin.site.register(Product, ProductAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Bag, BagAdmin)
admin.site.register(About, AboutAdmin)
admin.site.register(OurAdvantage, OurAdvantageAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Slider, SliderAdmin)
admin.site.register(PublicOffer, PublicOfferAdmin)
admin.site.register(Help, HelpAdmin)
admin.site.register(ImageHelp, ImageHelpAdmin)


