from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^(?P<pk>[0-9]+)/$', views.UserProfile.as_view(), ),
    url(r'^auth/$', views.auth, name='auth'),
    url(r'^create/$', views.create_user, name='create_user'),
    url(r'^update/(?P<pk>[0-9]+)/$', views.edit_user, name='update_user'),
    url(r'^delete/(?P<pk>[0-9]+)/$', views.delete_user, name='delete_user'),
    url(r'^login/$', views.login_user, name='weblogin'),
    url(r'^logout/$', views.logut_user, name='weblogout'),
    url(r'$', views.users_list, name='users'),

]