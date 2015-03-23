from django.conf.urls import patterns, include, url

urlpatterns = patterns('administracion.views', 
    url(r'administracion/$', 'home', name='home'),
    url(r'administracion/temporada$', 'temporada', name='temporada'),
    url(r'administracion/temporada/cierre$', 'cierre_temporada', name='cierre_temporada'),
    url(r'administracion/pagos$', 'ingreso', name='ingreso'),
    url(r'administracion/egresos$', 'egresos', name='egresos'),
    url(r'administracion/perfil/$','perfil',name='perfil'),
	url(r'administracion/junta_directiva/$','junta_directiva',name='junta_directiva'),
)