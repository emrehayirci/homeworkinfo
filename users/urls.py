from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^(?P<pk>[0-9]+)/$', views.UserProfile.as_view(), ),
    url(r'^auth/$', views.auth, name='auth'),
    url(r'^login/$', views.login, name='weblogin'),
]