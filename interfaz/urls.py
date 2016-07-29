from django.conf.urls import patterns, include, url
from monitoreo.views import data, iniciar_streamer_twitter, matarproceso, agregar_cuenta, agregar_hashtag, iniciar_streamer_hashtag, eliminar, eliminar_archivo, pasados
from usuario.views import login_user, logout_user
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
import settings
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', data),
    url(r'^iniciarstream/$',iniciar_streamer_twitter),
    url(r'^iniciarhashtag/$',iniciar_streamer_hashtag),
    url(r'^matarproceso/$',matarproceso),
    url(r'^login/$',login_user),
    url(r'^logout/$',logout_user),
    url(r'^agregarcuenta/$',agregar_cuenta),
    url(r'^agregarhashtag/$',agregar_hashtag),
    url(r'^eliminar/([CH][0-9A-Za-z]+)/$',eliminar),
    url(r'^eliminar_archivo/$',eliminar_archivo),
    url(r'^pasados/([CH][0-9A-Za-z]+)/$',pasados),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
