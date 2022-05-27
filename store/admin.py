from django.contrib import admin
from store.models import Product, Collection, ProductColor, ProductImage, AboutImage, About, OurAdvantage, News


class ProductAdmin(admin.ModelAdmin):
    pass


class CollectionAdmin(admin.ModelAdmin):
    pass


class ColorAdmin(admin.ModelAdmin):
    list_display = ['image', 'color']


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image']


class AboutAdmin(admin.ModelAdmin):
    pass


class AboutImageAdmin(admin.ModelAdmin):
    list_display = ['page', 'image']


class OurAdvantageAdmin(admin.ModelAdmin):
    list_display = ['headline', 'description', 'icon']


class NewsAdmin(admin.ModelAdmin):
    list_display = ['headline', 'description', 'photo']


admin.site.register(Product, ProductAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(ProductColor, ColorAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(AboutImage, AboutImageAdmin)
admin.site.register(About, AboutAdmin)
admin.site.register(OurAdvantage, OurAdvantageAdmin)
admin.site.register(News, NewsAdmin)
