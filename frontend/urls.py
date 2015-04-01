from django.conf.urls import patterns, include, url

urlpatterns = patterns('frontend.views',
	url(r'^$','index',name='index'),
	url(r'^/$','inicio',name='inicio'),
	url(r'^home/$','home',name='home'),
	url(r'^socios/$','socios',name='socios'),
	url(r'^socio/(?P<dni>\d+)$','socio',name='socio'),
	url(r'^contactenos/$','contactenos',name='contactenos'),
	url(r'^estatutos/$','estatutos',name='estatutos'),
	url(r'^informes/$','informes',name='informes'),
	url(r'^periodismo/$','periodismo',name='periodismo'),
	url(r'^reglamentos/$','reglamentos',name='reglamentos'),
)