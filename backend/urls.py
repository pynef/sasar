from django.conf.urls import patterns, include, url

urlpatterns = patterns('backend.views',
	url(r'administracion/$','index',name='index'),
	url(r'administracion/junta_directiva/$','junta_directiva',name='junta_directiva'),
    url(r'administracion/nueva_junta_directiva/$','nueva_junta_directiva',name='nueva_junta_directiva'),
    url(r'^administrador/edit_junta_directiva/(?P<id>\d+)$', 'edit_junta_directiva', name='edit_junta_directiva'),
    url(r'^administrador/borrar_junta_directiva/(?P<id>\d+)$', 'borrar_junta_directiva', name='borrar_junta_directiva'),
    url(r'administracion/$', 'homes', name='homes'),
    url(r'administracion/temporada$', 'temporada', name='temporada'),
    url(r'administracion/temporada/cierre$', 'cierre_temporada', name='cierre_temporada'),
    url(r'administracion/pagos$', 'ingreso', name='ingreso'),
    url(r'administracion/egresos$', 'egresos', name='egresos'),
    url(r'administracion/perfil/$','perfil',name='perfil'),
    url(r'administracion/galeria_imagenes/$','galeria_imagenes',name='galeria_imagenes'),
    url(r'^administrador/borrar_galeria_imagenes/(?P<id>\d+)$', 'borrar_galeria_imagenes', name='borrar_galeria_imagenes'),
    url(r'^administrador/edit_galeria_imagenes/(?P<id>\d+)$', 'edit_galeria_imagenes', name='edit_galeria_imagenes'),
    url(r'administracion/reporte_socio/$','reporte_socio',name='reporte_socio'),
    url(r'administracion/reporte_socio/(?P<id>\d+)$','reporte_socio',name='reporte_socio'),
    url(r'administracion/reporte_ingresos/$','reporte_ingresos',name='reporte_ingresos'),
    url(r'administracion/reporte_egresos/$','reporte_egresos',name='reporte_egresos'),
    url(r'administracion/reporte_general/$','reporte_general',name='reporte_general'),
    url(r'administracion/galeria_video/$','galeria_video',name='galeria_video'),
    url(r'administracion/socio_back/(?P<dni>\d+)$','socio_back',name='socio_back'),
    url(r'administracion/nuevo_socio/$','nuevo_socio',name='nuevo_socio'),
    url(r'administracion/desactivo/$','desactivo',name='desactivo'),
    url(r'administracion/noticias/$','noticias',name='noticias'),
    url(r'administracion/edit_noticias/(?P<id>\d+)$','edit_noticias',name='edit_noticias'),
    url(r'administracion/del_noticias/(?P<id>\d+)$','del_noticias',name='del_noticias'),
    url(r'administracion/banner/$','banner',name='banner'),
    url(r'administracion/edit_banner/(?P<id>\d+)$','edit_banner',name='edit_banner'),
    url(r'administracion/del_banner/(?P<id>\d+)$','del_banner',name='del_banner'),
    url(r'administracion/galeria_fotos/$','galeria_fotos',name='galeria_fotos'),
    url(r'^administracion/borrar_fotos/(?P<id>\d+)$', 'borrar_fotos', name='borrar_fotos'),
    url(r'^administracion/edit_fotos/(?P<id>\d+)$', 'edit_fotos', name='edit_fotos'),
    url(r'^administracion/activar_socio/$', 'activar_socio', name='activar_socio'),
)
