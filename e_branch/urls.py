from django.conf.urls import url

from .views import *

urlpatterns = [
    # url(r'^(?P<pk>[0-9]+)/$', views.UserProfile.as_view(), ),
    url(r'^$', views.settings, name='settings'),

]