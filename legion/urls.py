from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^',include('frontend.urls')),
    url(r'^',include('backend.urls')),
    url(r'^',include('administracion.urls')),
    url(r'^media/(?P<path>.*)$','django.views.static.serve',
    			{'document_root':settings.MEDIA_ROOT,}
    	),
    url(r'^login/$', 'django.contrib.auth.views.login',{'template_name':'login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),

    url(r'^panel/clave/$','django.contrib.auth.views.password_change',
        {'template_name': 'registration/password_reset.html'}, name="password_reset" ),
    url(r'^panel/clave/done$','django.contrib.auth.views.password_change_done',
        {'template_name': 'registration/password_done.html'}, name="password_change_done"),
)
urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATIC_ROOT}),
)