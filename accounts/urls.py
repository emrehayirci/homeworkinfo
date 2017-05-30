from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    # url(r'^(?P<pk>[0-9]+)/$', views.UserProfile.as_view(), )
    url(r'^create/$', views.create_account, name='create_account'),
    url(r'^delete/(?P<pk>[0-9]+)/$', views.account_delete, name='account_delete'),
    url(r'^create_currrency/$', views.add_currency, name='add_currency'),
    url(r'currency_list/$', views.currency_list, name='currency_list'),
    url(r'^update/(?P<pk>[0-9]+)/$', views.account_update, name='account_update'),
    url(r'^update_currency/(?P<pk>[0-9]+)/$', views.update_currency, name='currency_update'),
    url(r'^delete_currency/(?P<pk>[0-9]+)/$', views.delete_currency, name='currency_delete'),
    url(r'^transaction/(?P<pk>[0-9]+)/$', views.cancel_transaction, name='cancel_transaction'),
    url(r'^transaction/delete/(?P<pk>[0-9]+)/$', views.delete_transaction, name='delete_transaction'),
    url(r'^transaction/api/$', views.api_transaction),
    url(r'^query/receipt/(?P<pk>[0-9]+)/$', views.query_receipt,),
    url(r'^transactions/$', views.transactions_list, name='transactions_a'),
    url(r'^loan/(?P<pk>[0-9]+)/$', views.loan_detail, name='loan_detail'),
    url(r'^loan/pay/(?P<pk>[0-9]+)/$', views.pay, name='pay'),
    url(r'^loans/$', views.loan_list, name='loans_a'),
    url(r'$', views.settings, name='settings'),
    
]