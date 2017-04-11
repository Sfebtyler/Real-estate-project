from django.core.mail import send_mail
from app.models import Home, Favorites, ExtraImage, ContactInfo, EmailSettings, UserModel
from rest_framework import serializers
import uuid


class FavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = ('id', 'user', 'list')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'phone', 'temp_token')

    def create(self, validated_data):
        password = self.context['request'].data['password']
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(password)
        user.save()
        return user


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
        fields = ('image', 'listed_agent_name', 'listed_phone_number', 'listed_email', 'company_info')


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


class PasswordResetSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    to_email = serializers.EmailField()

    def create(self, validated_data):
        print(UserModel.objects.get(email=validated_data['to_email']))
        # creating temporary token
        UserModel.objects.filter(email=validated_data['to_email']).update(temp_token=uuid.uuid4().hex)
        # token that is being sent through email
        token = UserModel.objects.get(email=validated_data['to_email']).temp_token
        emailsubject = 'Password Reset for SGRealty.com'
        message = 'please click the following link in order to reset your password http://localhost:3000/passwordreset/'\
                  + token
        from_email = EmailSettings.objects.first().from_email
        send_to_email = [validated_data['to_email']]

        send_mail(
            emailsubject,
            message,
            from_email,
            send_to_email,
            fail_silently=True,
        )
        return 'password reset email sent!'
