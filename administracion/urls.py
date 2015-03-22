from django.conf.urls import patterns, include, url

urlpatterns = patterns('administracion.views', 
    url(r'administracion/$', 'home', name='home'),
    url(r'administracion/temporada$', 'temporada', name='temporada'),
    url(r'administracion/temporada/cierre$', 'cierre_temporada', name='cierre_temporada'),
)