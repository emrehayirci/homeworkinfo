from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^login/$', login, name='login'),
    url(r'^accounts/', accounts, name='accounts'),
    url(r'^register/', register, name='register'),
    url(r'^$', index, name='index'),
]