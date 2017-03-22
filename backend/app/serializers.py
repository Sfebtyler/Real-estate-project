from django.contrib.auth.models import User
from django.core.mail import send_mail
from app.models import Home, Favorites, ExtraImage, ContactInfo, EmailSettings, Profile
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        u = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        u.set_password(validated_data['password'])
        u.save()
        print(u)
        p = Profile(
            user=u,
            phone_number=self.context['request'].data['phone_number']
        )
        p.save()
        return u


class UserReadSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        exclude = ('password', )


class ProfileSerializer(serializers.ModelSerializer):
    user = UserReadSerializer(many=False, read_only=True)

    class Meta:
        model = Profile
        fields = ('user', 'phone_number')


class FavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = ('id', 'user', 'list')


class ExtraImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ExtraImage
        fields = ('additionalimage', 'home', 'description')


class HomeSerializer(serializers.HyperlinkedModelSerializer):
    image = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()

    def get_image(self, obj):
        if not obj.image:
            return None
        return self.context['request'].build_absolute_uri(obj.image.url)

    def get_is_favorite(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.favorites_set.filter(user=user).exists()
        else:
            return False

    class Meta:
        model = Home
        fields = ('id', 'title', 'city', 'state', 'street', 'price', 'mls_number', 'sold', 'is_premium', 'image',
                  'is_favorite')


class ContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = ('listed_agent_name', 'listed_phone_number', 'listed_email')


class EmailSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailSettings


class Contact(object):
    def __init__(self, name, subject, email, text):
        self.name = name
        self.subject = subject
        self.email = email
        self.text = text


class EmailSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    name = serializers.CharField()
    subject = serializers.CharField()
    email = serializers.EmailField()
    text = serializers.CharField()

    def create(self, validated_data):

        guestname = validated_data['name']
        emailsubject = validated_data['subject']
        message = validated_data['text']
        from_email = EmailSettings.objects.first().from_email
        to_email = [EmailSettings.objects.first().to_email]

        send_mail(
            'Message from {}: {}'.format(guestname, emailsubject),
            message,
            from_email,
            to_email,
            fail_silently=True,
        )
        return Contact(**validated_data)
