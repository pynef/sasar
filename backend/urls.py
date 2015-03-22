from django.conf.urls import patterns, include, url

urlpatterns = patterns('backend.views',
	url(r'panel/$','index',name='index'),
	url(r'panel/perfil/$','perfil',name='perfil'),
	url(r'panel/junta_directiva/$','junta_directiva',name='junta_directiva'),
)