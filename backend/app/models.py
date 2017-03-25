from django.db import models
from django.conf import settings
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import UserManager
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


class UserModel(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(blank=False)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=20)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_active = models.BooleanField(default=True)

    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'
    objects = UserManager()

    def get_full_name(self):
        full_name = '{} {}'.format(self.first_name, self.last_name).strip()
        return full_name or self.email

    def get_short_name(self):
        return self.first_name or self.email

    class Meta:
        verbose_name_plural = 'Users'


class ExtraImage(models.Model):
    home = models.ForeignKey('Home', null=True, blank=True)
    additionalimage = models.ImageField(upload_to='images')
    description = models.TextField(default='', null=True, blank=True)


class MLSNumber(models.Model):
    home_id = models.ForeignKey('Home', null=True, blank=True)
    number = models.CharField(null=True, blank=True, max_length=50)

    def __str__(self):
        return self.number


class Home(models.Model):
    title = models.TextField(default='')
    city = models.TextField(default='')
    state = models.TextField(default='')
    street = models.TextField(default='')
    price = models.IntegerField(default='')
    sold = models.BooleanField(default=False)
    numofbeds = models.CharField(default='', max_length=10000, blank=True)
    numofbaths = models.CharField(default='', max_length=10000, blank=True)
    is_premium = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    published = models.BooleanField(default=False)
    thumbnail = ImageSpecField(source='image', processors=[ResizeToFill(100, 100)],
                                      options={'quality': 60})

    def __str__(self):
        return self.title

    def get_url(self):
        return self.image.url

    def mls_number(self):
        return ", ".join([n.number for n in self.mlsnumber_set.all()])


class Favorites(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    list = models.ForeignKey(Home, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'list',)


class ContactInfo(models.Model):
    listed_agent_name = models.CharField(max_length=20)
    listed_email = models.EmailField()
    listed_phone_number = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = 'Contact Info'

    def save(self, *args, **kwargs):
        ContactInfo.objects.all().delete()
        super(ContactInfo, self).save(*args, **kwargs)
        return


class EmailSettings(models.Model):
    from_email = models.EmailField(null=True)
    to_email = models.EmailField(null=True)

    class Meta:
        verbose_name_plural = 'Email Settings'

    def save(self, *args, **kwargs):
        EmailSettings.objects.all().delete()
        super(EmailSettings, self).save(*args, **kwargs)
        return
