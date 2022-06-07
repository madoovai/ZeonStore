from django.contrib import admin
from store.models import ProductLine, Collection, ProductImage, AboutImage, About, OurAdvantage, News, \
    PublicOffer, Help, ImageHelp, Color, Slider, ShoppingCart, Order, Footer, SecondFooter, OrderItem


class ImageAdminInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    max_num = 8


class ProductLineAdmin(admin.ModelAdmin):
    inlines = [ImageAdminInline]


class CollectionAdmin(admin.ModelAdmin):
    pass


class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'rgb']


class AboutImageAdminInline(admin.TabularInline):
    model = AboutImage
    extra = 0
    max_num = 3


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ['product', 'color', 'total_old_price', 'total_discount_price',
                    'size_line', 'image', 'amount_of_productline']


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'color', 'total_old_price', 'total_discount_price',
                    'size_line', 'image', 'amount_of_productline']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['name', 'order_date', 'order_status', 'amount_of_productlines', 'total_number_of_products', 'total_price_without_discount',
                    'total_price_with_discount', 'final_total_price']


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


class SecondFooterAdminInline(admin.TabularInline):
    model = SecondFooter
    extra = 0
    readonly_fields = ['link']


class FooterAdmin(admin.ModelAdmin):
    inlines = [SecondFooterAdminInline]
    list_display = ['text_info', 'phone_number']


admin.site.register(ProductLine, ProductLineAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(About, AboutAdmin)
admin.site.register(OurAdvantage, OurAdvantageAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Slider, SliderAdmin)
admin.site.register(PublicOffer, PublicOfferAdmin)
admin.site.register(Help, HelpAdmin)
admin.site.register(ImageHelp, ImageHelpAdmin)
admin.site.register(Footer, FooterAdmin)


