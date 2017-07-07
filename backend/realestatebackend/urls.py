from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from app import views

urlpatterns = [

    url(r'^$', views.PremiumHomeTemplateView.as_view(), name='mainpage'),
    url(r'^homes/$', views.HomeTemplateView.as_view(), name='homes'),
    url(r'^homes/(?P<id>[0-9]+)/$', views.HomeDetailsTemplateView.as_view(), name='details'),
    url(r'^favorites/$', views.FavoritesHomeTemplateView.as_view(), name='favorites'),
    url(r'^contacts/', views.ContactsTemplateView.as_view(), name='contacts'),
    url(r'^search/', views.SearchHomesTemplateView.as_view(), name='search'),
    url(r'^admin/', admin.site.urls),
    url(r'^user_login/', views.UserLogin.as_view(), name='user_login'),
    url(r'^logout/$', views.UserLogout.as_view(), name='logout'),
    url(r'^create-account/$', views.UserCreateTemplateView.as_view(), name='create-account'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
