from django.contrib import admin
from imagekit.admin import AdminThumbnail
from app.models import Home, ExtraImage, MLSNumber, ContactInfo, EmailSettings, Profile
import re


admin.site.site_header = 'SGRealty Site Administration'


class ExtraImagesInline(admin.TabularInline):
    model = ExtraImage


class MLSNumbersInline(admin.TabularInline):
    model = MLSNumber


class HomeAdmin(admin.ModelAdmin):
    def get_modded_price(self, Home):
        if Home.price:
            changed_price = re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1,", "%d" % Home.price)
            return '$' + changed_price
        else:
            return 'No price given'

    get_modded_price.short_description = 'price'

    search_fields = ('id', 'title', 'city', 'street', 'mlsnumber__number', 'numofbeds', 'numofbaths')
    list_display = ('id', 'admin_thumbnail', '__str__', 'street', 'city', 'mls_number', 'get_modded_price', 'is_premium',
                    'sold', 'published')
    admin_thumbnail = AdminThumbnail(image_field='thumbnail')
    readonly_fields = ['thumbnail']

    inlines = [
        MLSNumbersInline,
        ExtraImagesInline,
    ]


admin.site.register(Home, HomeAdmin)
admin.site.register(ContactInfo)
admin.site.register(EmailSettings)
admin.site.register(Profile)