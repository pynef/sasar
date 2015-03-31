#-*- coding:utf-8 -*-

from django.contrib.auth.models import User,Group
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse

def backend_login(view_func):
    def wrap(request, *args, **kwargs):
        is_sec = request.user.groups.filter(name='backend').count()
        if request.user.is_authenticated() and is_sec :
            return view_func( request=request,*args, **kwargs )
        return HttpResponseRedirect(reverse('index'))
    wrap.__doc__ = view_func.__doc__
    wrap.__dict__ = view_func.__dict__
    return wrap

def frontend_login(view_func):
    def wrap(request, *args, **kwargs):
        is_doc = request.user.groups.filter(name='frontend').count()
        if request.user.is_authenticated() and is_doc :
            return view_func( request=request,*args, **kwargs )
        return HttpResponseRedirect(reverse('index'))
    wrap.__doc__ = view_func.__doc__
    wrap.__dict__ = view_func.__dict__
    return wrap
