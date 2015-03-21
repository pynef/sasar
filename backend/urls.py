from django.conf.urls import patterns, include, url

urlpatterns = patterns('backend.views',
	url(r'^panel/$','index',name='index'),
	url(r'^panel/profile/$','profile',name='profile'),
)