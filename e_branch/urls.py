from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^login/$', login, name='login'),
    url(r'^register/', register, name='register'),
    url(r'^accounts/', accounts, name='accounts'),
    url(r'^loans/', loans, name='loans'),
    url(r'^transactions/', transactions, name='transactions'),
    url(r'^$', index, name='index'),
]