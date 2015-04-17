from django.conf.urls import patterns, include, url

urlpatterns = patterns('frontend.views',
	url(r'^$','index',name='index'),
	url(r'^/$','inicio',name='inicio'),
	url(r'^home/$','home',name='home'),
	url(r'^socios/$','socios',name='socios'),
	url(r'^socio/(?P<dni>\d+)$','socio',name='socio'),
	url(r'^responsabilidad_social/$','responsabilidad_social',name='responsabilidad_social'),
	url(r'^estatutos/$','estatutos',name='estatutos'),
	url(r'^informes/$','informes',name='informes'),
	url(r'^periodismo/$','periodismo',name='periodismo'),
	url(r'^reglamentos/$','reglamentos',name='reglamentos'),
	url(r'^quienes_somos/$','quienes_somos',name='quienes_somos'),
	url(r'^las_noticias/$','las_noticias',name='las_noticias'),
	url(r'^galeria_de_fotos/$','galeria_de_fotos',name='galeria_de_fotos'),
	url(r'^fotos_socios/$','fotos_socios',name='fotos_socios'),
	url(r'^fotos_galeria/$','fotos_galeria',name='fotos_galeria'),
	url(r'^videos_galeria/$','videos_galeria',name='videos_galeria'),
)