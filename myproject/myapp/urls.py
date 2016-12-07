# -*- coding: utf-8 -*-
#from django.conf.urls import url
#from . import views
#
#
#urlpatterns = ('myproject.myapp.views', #REMOVED ¿?
#    url(r'^list/$', 'list', name='list'),
#    url(r'^configuration/$', 'configuration', name='configuration'),
#    url(r'^givemepiece/$', 'givemepiece', name='givemepiece'),
#    url(r'^sendpiece/$', 'sendpiece', name='sendpiece'),
#    #url(r'^(?P<thread_id>[0-9]+)/$', views.thread, name='thread'),
#    url(r'^(?P<thread_id>[0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM]+)/$', views.thread, name='thread'),
#)

from django.conf.urls import url
from . import views as myapp_views
from django.conf.urls import include

urlpatterns = (
    url(r'^list/$', myapp_views.list, name='list'),
    url(r'^configuration/$', myapp_views.configuration, name='configuration'),
    url(r'^givemepiece/$', myapp_views.givemepiece, name='givemepiece'),
    url(r'^sendpiece/$', myapp_views.sendpiece, name='sendpiece'),
    url(r'^administrate/$', myapp_views.administrate, name='administrate'),
    url(r'^captcha/', include('captcha.urls')),
    #url(r'^pruebaconfig/$', myapp_views.pruebaconfig, name='pruebaconfig'), #debug config.html
    #url(r'^pruebamessage/$', myapp_views.pruebainfomessage, name='pruebainfomessage'), #debug infomessage.html
    url(r'^(?P<thread_id>[0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM]+)/', myapp_views.thread, name='thread')
)