from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from app.models import Home, Favorites, ExtraImage, ContactInfo
from rest_framework import viewsets, serializers
from rest_framework.decorators import list_route, detail_route
from rest_framework import status
from app.serializers import UserSerializer, HomeSerializer, FavoritesSerializer, ExtraImageSerializer, \
    EmailSerializer, ContactInfoSerializer
from rest_framework.response import Response
from django.db.models import Q


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = []

    @list_route(methods=['GET'], permission_classes=[])
    def current_user(self, request, *args, **kwargs):
        if request.user:
            serializer = self.get_serializer(instance=request.user)
            return Response(serializer.data)
        else:
            return Response({'error': 'Not logged in!'}, status=status.HTTP_401_UNAUTHORIZED)


class EmailViewSet(viewsets.ViewSet):
    serializer_class = EmailSerializer

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
        qset = self.queryset.prefetch_related('favorites_set__user')
        params = self.request.query_params
        if 'premium_homes' in params:
            qset = qset.filter(is_premium=True)

        if 'favorites' in params:
            print(self.request.user)
            qset = qset.filter(favorites__user=self.request.user)

        if 'q' in params:
            # Poor mans search endpoint
            moddablesearchterm = params['q']
            search_term = moddablesearchterm.strip()

            if not search_term or len(search_term) <= 2:
                raise serializers.ValidationError('Search Term must be at least 3 characters')

            qset = qset.filter(
                Q(title__icontains=search_term) |
                Q(city__icontains=search_term) |
                Q(street__icontains=search_term) |
                Q(mlsnumber__number__icontains=search_term)
            )
        return qset


class FavoritesViewSet(viewsets.ModelViewSet):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer
    permission_classes = [IsAuthenticated]

