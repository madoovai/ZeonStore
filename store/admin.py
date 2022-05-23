from django.contrib import admin
from store.models import Product, Collection


class ProductAdmin(admin.ModelAdmin):
    pass


class CollectionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Product, ProductAdmin)
admin.site.register(Collection, CollectionAdmin)