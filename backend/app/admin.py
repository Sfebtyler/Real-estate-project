from django.contrib import admin
from imagekit.admin import AdminThumbnail
from app.models import Home, ExtraImage, MLSNumber, ContactInfo, EmailSettings, UserModel
import re
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

admin.site.site_header = 'SGRealty Site Administration'


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = UserModel
        fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'is_staff', 'is_superuser')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = UserModel
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'phone', 'is_staff', 'is_superuser', 'is_active')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'email', 'phone', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


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
admin.site.register(UserModel, UserAdmin)
