'''Shorty URLs'''
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.do_redirect, name='redirect_base'),
    url(r'^delete/$', views.delete, name='delete'),
    url(r'^admin/$', views.home, name='home'),
    url(r'^(?P<slug>[-_\w]+)$', views.do_redirect, name='redirect'),
]
