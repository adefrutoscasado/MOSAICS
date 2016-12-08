from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

#from django.views.generic import RedirectView


from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^project', include('myproject.myapp.urls')),
    url(r'^$', RedirectView.as_view(url='/project/list/', permanent=True)),

    #url(r'', RedirectView.as_view(url='/project/list/', permanent=True)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ambos dirigen de forma erronea:
# url(r'^/', RedirectView.as_view(url='/project/list/', permanent=True)),
# url(r'^', RedirectView.as_view(url='/project/list/', permanent=True)),