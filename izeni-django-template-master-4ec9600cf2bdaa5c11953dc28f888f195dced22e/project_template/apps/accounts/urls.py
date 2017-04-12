from django.conf.urls import url
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^login/$', auth_views.login, name='login',
        kwargs={'extra_context': {'site_name': '{{ project_name }}'}}),
    url(r'^logout/$', auth_views.logout, name='logout',
        kwargs={'next_page': '/',
                'extra_context': {'site_name': '{{ project_name }}'}}),
]
