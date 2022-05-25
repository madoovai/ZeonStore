from django.contrib import admin
from store.models import Product, Collection, ProductColor, ProductSizeLine, ProductImage


class ProductAdmin(admin.ModelAdmin):
    pass


class CollectionAdmin(admin.ModelAdmin):
    pass


class ColorAdmin(admin.ModelAdmin):
    list_display = ['product', 'color']


class SizeLineAdmin(admin.ModelAdmin):
    list_display = ['product', 'size']


class ProductImageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Product, ProductAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(ProductColor, ColorAdmin)
admin.site.register(ProductSizeLine, SizeLineAdmin)
admin.site.register(ProductImage, ProductImageAdmin)