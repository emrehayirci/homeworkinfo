from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^(?P<pk>[0-9]+)/$', views.UserProfile.as_view(), ),
    url(r'^$', views.settings, name='settings'),
    url(r'^create/$', views.create_account, name='create_account'),
    url(r'^delete/(?P<pk>[0-9]+)/$', views.account_delete, name='account_delete'),
    url(r'^create_currrency/$', views.add_currency, name='add_currency'),
    url(r'currency_list/$', views.currency_list, name='currency_list'),
    url(r'^update/(?P<pk>[0-9]+)/$', views.account_update, name='account_update'),
    url(r'^update_currency/(?P<pk>[0-9]+)/$', views.update_currency, name='currency_update'),
    url(r'^delete_currency/(?P<pk>[0-9]+)/$', views.delete_currency, name='currency_delete'),
    
]