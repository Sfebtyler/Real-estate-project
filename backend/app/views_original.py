from rest_framework.permissions import IsAuthenticated, AllowAny
from app.models import Home, Favorites, ExtraImage, ContactInfo, UserModel
from rest_framework import viewsets
from rest_framework.decorators import list_route, detail_route
from rest_framework import status
from app.serializers import UserSerializer, HomeSerializer, FavoritesSerializer, ExtraImageSerializer, \
    EmailSerializer, ContactInfoSerializer, PasswordResetSerializer
from rest_framework.response import Response
from django.db.models import Q
from django.views import generic as generic_views
from django.views.generic import DetailView
from django.core.urlresolvers import reverse

class UserViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = []

    @list_route(methods=['GET'], permission_classes=[])
    def current_user(self, request, *args, **kwargs):
        if request.user:
            print('REQUEST', request.user)
            tmpProfile = UserModel.objects.filter(id=request.user.id).first()
            if tmpProfile:
                userprofile = UserSerializer(instance=tmpProfile, context={'request': request}).data
                print('profile', userprofile)
                return Response(userprofile)
            else:
                return Response({'error': 'Profile does not exist!'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Not logged in!'}, status=status.HTTP_401_UNAUTHORIZED)

    @list_route(methods=['GET'])
    def check_if_user_exists(self, instance):
        params = self.request.query_params
        username = params['q']
        if len(UserModel.objects.filter(username=username)) > 0:
            return Response("Username already in use!")
        else:
            return Response("Username is available!")

    @list_route(methods=['GET'])
    def check_if_email_exists(self, instance):
        params = self.request.query_params
        email = params['q']
        if len(UserModel.objects.filter(email=email)) > 0:
            return Response("Email already in use!")
        else:
            return Response("Email is available!")


class PasswordResetViewSet(viewsets.ViewSet):
    serializer_class = EmailSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @list_route(methods=['POST'])
    def confirm_reset(self, request):
        token = request.data['temptoken']['id']
        password = request.data['password']
        user = UserModel.objects.get(temp_token=token)
        print('temp token', token)
        print('user of token', user)
        if len(UserModel.objects.filter(temp_token=token)) > 0:
            if len(password) > 8:
                user.set_password(password)
                user.temp_token = ''
                user.save()
                return Response('Password updated')
            else:
                return Response('Invalid Password', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('Password reset email has expired or token is invalid. Please try again.')


class EmailViewSet(viewsets.ViewSet):
    serializer_class = EmailSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContactInfoViewSet(viewsets.ModelViewSet):
    queryset = ContactInfo.objects.all()
    serializer_class = ContactInfoSerializer
    permission_classes = (AllowAny,)


class HomeViewSet(viewsets.ModelViewSet):
    template_name = 'main_page/main_page.html'
    context_object_name = 'homes_list'
    queryset = Home.objects.filter(published=True)
    serializer_class = HomeSerializer
    permission_classes = (AllowAny,)

    @detail_route(methods=['Get'], permission_classes=[])
    def extra_images(self, request, pk):
        image = ExtraImage.objects.all().filter(home=pk)
        serializer = ExtraImageSerializer(image, many=True, context={'request': request})
        return Response(serializer.data)

    @list_route(methods=['Post'])
    def delete_favorite(self, request):
        Favorites.objects.filter(list__in=request.data.get('list'), user=self.request.user).delete()

        return Response(status=status.HTTP_200_OK)

    def get_queryset(self):
        if self.request.user != 'undefined':
            qset = self.queryset.prefetch_related('favorites_set__user')
        else:
            qset = Home.objects.all()
        params = self.request.query_params
        user = self.request.user
        if 'premium_homes' in params:
            qset = qset.filter(is_premium=True)

        if 'favorites' in params:
            print('id', user)
            qset = qset.filter(favorites__user=user)

        if 'totalbeds' in params and params['totalbeds'] != '':
            qset = qset.filter(
                Q(numofbeds__icontains=params['totalbeds'])
                              )

        if 'totalbaths' in params and params['totalbaths'] != '':
            qset = qset.filter(Q(numofbaths__icontains=params['totalbaths'])
                            )

        if 'pricerangestart' in params and params['pricerangestart'] != '':
            qset = qset.filter(Q(price__gte=params['pricerangestart'])
                            )

        if 'pricerangestop' in params and params['pricerangestop'] != '':
            qset = qset.filter(Q(price__lte=params['pricerangestop'])
                            )

        if 'pricerangestart' in params and 'pricerangestop' in params and params['pricerangestart'] != '' and \
                params['pricerangestop'] != '':
            qset = qset.filter(Q(price__range=(params['pricerangestart'], params['pricerangestop'])))

        if 'q' in params:
            # Poor mans search endpoint
            moddablesearchterm = params['q']
            search_term = moddablesearchterm.strip()

            qset = qset.filter(
                Q(title__icontains=search_term) |
                Q(city__icontains=search_term) |
                Q(street__icontains=search_term) |
                Q(mlsnumber__number__icontains=search_term)
            )
        return qset.distinct()

class FavoritesViewSet(viewsets.ModelViewSet):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer
    permission_classes = [IsAuthenticated]

