from django.conf.urls import patterns, include, url

urlpatterns = patterns('frontend.views',
	url(r'^$','index',name='index'),
	url(r'^/$','inicio',name='inicio'),
	url(r'^home/$','home',name='home'),
	url(r'^nosotros/$','nosotros',name='nosotros'),
	url(r'^socio/(?P<dni>\d+)$','socio',name='socio'),
)