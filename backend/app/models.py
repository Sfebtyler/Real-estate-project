from django.db import models
from django.conf import settings
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12, null=True)


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
    leads_from_email = models.EmailField()
    leads_to_email = models.EmailField()

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
