from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework import routers
from rest_framework.authtoken import views as authview

from app import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'homes', views.HomeViewSet)
router.register(r'favorites', views.FavoritesViewSet)
router.register(r'contact-us', views.EmailViewSet, 'contact-us')
router.register(r'contacts', views.ContactInfoViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-token-auth/', authview.obtain_auth_token),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
