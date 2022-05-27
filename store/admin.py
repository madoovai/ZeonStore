from django.contrib import admin
from store.models import Product, Collection, ProductColor, ProductImage, AboutImage, About


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


admin.site.register(Product, ProductAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(ProductColor, ColorAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(AboutImage, AboutImageAdmin)
admin.site.register(About, AboutAdmin)
