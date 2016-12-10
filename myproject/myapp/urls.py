# -*- coding: utf-8 -*-
#from django.conf.urls import url
#from . import views
#
#


from django.conf.urls import url
from . import views as myapp_views
from django.conf.urls import include

urlpatterns = (
    url(r'^/configuration/$', myapp_views.configuration, name='configuration'),
    url(r'^/givemepiece/$', myapp_views.givemepiece, name='givemepiece'),
    url(r'^/sendpiece/$', myapp_views.sendpiece, name='sendpiece'),
    url(r'^/administrate/$', myapp_views.administrate, name='administrate'),
    url(r'^captcha/', include('captcha.urls')),
    #url(r'^pruebaconfig/$', myapp_views.pruebaconfig, name='pruebaconfig'), #debug config.html
    #url(r'^pruebamessage/$', myapp_views.pruebainfomessage, name='pruebainfomessage'), #debug infomessage.html
    url(r'^/list/$', myapp_views.listofprojects, name='list'),
    url(r'^/(?P<thread_id>[0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM]+)/', myapp_views.thread, name='thread')

)