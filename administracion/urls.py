from django.conf.urls import patterns, include, url

urlpatterns = patterns('administracion.views', 
    url(r'administracion^/$', 'home', name='home')
    )