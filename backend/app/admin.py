from django.contrib import admin
from imagekit.admin import AdminThumbnail
from app.models import Home, ExtraImage, MLSNumber, ContactInfo, EmailSettings


class ExtraImagesInline(admin.TabularInline):
    model = ExtraImage


class MLSNumbersInline(admin.TabularInline):
    model = MLSNumber


class HomeAdmin(admin.ModelAdmin):

    search_fields = ('id', 'title', 'city', 'street', 'mlsnumber__number')
    list_display = ('id', 'admin_thumbnail', '__str__', 'street', 'city', 'mls_number', 'price', 'is_premium',
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