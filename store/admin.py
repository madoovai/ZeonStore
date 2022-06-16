from django.contrib import admin
from django.shortcuts import redirect

from store.models import ProductLine, Collection, ProductImage, AboutImage, About, OurAdvantage, News, \
    PublicOffer, Help, ImageHelp, Color, Slider, ShoppingCart, Order, Footer, SecondFooter, OrderItem, CallBack, \
    UserFavoriteProduct


class ImageAdminInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    max_num = 8


class ProductLineAdmin(admin.ModelAdmin):
    inlines = [ImageAdminInline]


class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'image']


class ColorAdmin(admin.ModelAdmin):
    model = Color
    list_display = ['name', 'rgb']

    def has_add_permission(self, request):
        return Color.objects.all().count() == 7


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'color', 'old_price', 'discount_price',
                    'size_line', 'image', 'amount_of_productline']


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'color', 'old_price', 'discount_price',
                    'size_line', 'image', 'amount_of_productline']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['name', 'order_date', 'order_status', 'amount_of_productlines', 'total_number_of_products', 'total_price_without_discount',
                    'total_discount', 'final_total_price']


class AboutImageAdminInline(admin.TabularInline):
    model = AboutImage
    extra = 0
    max_num = 3


class AboutAdmin(admin.ModelAdmin):
    inlines = [AboutImageAdminInline]

    def has_add_permission(self, request):
        return About.objects.all().count() == 0

    def changelist_view(self, request, extra_context=None):
        if About.objects.all().count() == 0:
            return redirect(request.path + "add/")
        else:
            about_us = About.objects.all().first()
            return redirect(request.path + f"{about_us.id}")


class OurAdvantageAdmin(admin.ModelAdmin):
    list_display = ['headline', 'description', 'icon']


class NewsAdmin(admin.ModelAdmin):
    list_display = ['headline', 'description', 'photo']


class SliderAdmin(admin.ModelAdmin):
    list_display = ['photo', 'link']

    def has_add_permission(self, request):
        return Slider.objects.all().count() == 0

    def changelist_view(self, request, extra_context=None):
        if Slider.objects.all().count() == 0:
            return redirect(request.path + "add/")
        else:
            slider = Slider.objects.all().first()
            return redirect(request.path + f"{slider.id}")


class PublicOfferAdmin(admin.ModelAdmin):
    list_display = ['headline', 'description']

    def has_add_permission(self, request):
        return PublicOffer.objects.all().count() == 0

    def changelist_view(self, request, extra_context=None):
        if PublicOffer.objects.all().count() == 0:
            return redirect(request.path + "add/")
        else:
            public_offer = PublicOffer.objects.all().first()
            return redirect(request.path + f"{public_offer.id}/")


class ImageHelpAdmin(admin.ModelAdmin):
    list_display = ['image']

    def has_add_permission(self, request):
        return ImageHelp.objects.all().count() == 0

    def changelist_view(self, request, extra_context=None):
        if ImageHelp.objects.all().count() == 0:
            return redirect(request.path + "add/")
        else:
            help_image = ImageHelp.objects.all().first()
            return redirect(request.path + f"{help_image.id}/")


class HelpAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer']


class SecondFooterAdminInline(admin.TabularInline):
    model = SecondFooter
    extra = 0
    max_num = 5
    list_display = ['input_field']


class FooterAdmin(admin.ModelAdmin):
    inlines = [SecondFooterAdminInline]
    list_display = ['text_info', 'phone_number']

    def has_add_permission(self, request):
        return Footer.objects.all().count() == 0

    def changelist_view(self, request, extra_context=None):
        if Footer.objects.all().count() == 0:
            return redirect(request.path + "add/")
        else:
            footer = Footer.objects.all().first()
            return redirect(request.path + f"{footer.id}/")


class CallBackAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone_number', 'call_received_date', 'callback_type', 'called_back']
    search_fields = ['name', 'phone_number']
    list_filter = ['called_back']


class UserFavoriteProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'productline_id']


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
admin.site.register(CallBack, CallBackAdmin)
admin.site.register(UserFavoriteProduct, UserFavoriteProductAdmin)
