#-*- coding:utf-8 -*-

from django.contrib.auth.models import User,Group
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from backend.models import Apertura, JuntaDirectiva, Cargo, Socio

def apertura_inactiva(view_func):
    def wrap(request, *args, **kwargs):
        is_sec = request.user.groups.filter(name='backend').count()
        ultima_apertura = Apertura.objects.all().order_by('-id')[0]
        print "ultima_apertura"
        print ultima_apertura
        apertura = JuntaDirectiva.objects.filter(socio=Socio.objects.get(id=request.user.id)).filter(apertura=ultima_apertura).filter(cargo=1)
        print "apertura"
        print apertura
        if apertura:
            if request.user.is_authenticated() and is_sec :
                return view_func( request=request,*args, **kwargs )
        else:
            return HttpResponseRedirect(reverse('index'))
    wrap.__doc__ = view_func.__doc__
    wrap.__dict__ = view_func.__dict__
    return wrap


def apertura_activa(view_func):
    def wrap(request, *args, **kwargs):
        apertura = Apertura.objects.filter(is_active=True)
        if not apertura:
            return HttpResponseRedirect(reverse('desactivo'))
        return view_func( request=request,*args, **kwargs )
    wrap.__doc__ = view_func.__doc__
    wrap.__dict__ = view_func.__dict__
    return wrap

def presidente(view_func):
    def wrap(request, *args, **kwargs):
        is_sec = request.user.groups.filter(name='backend').count()
        apertura = JuntaDirectiva.objects.filter(socio=Socio.objects.get(id=is_sec)).filter(apertura__is_active=True).filter(cargo=Cargo.objects.get(id=1))
        if not apertura:
            return HttpResponseRedirect(reverse('index'))
        return view_func( request=request,*args, **kwargs )
    wrap.__doc__ = view_func.__doc__
    wrap.__dict__ = view_func.__dict__
    return wrap

def backend_login(view_func):
    def wrap(request, *args, **kwargs):
        is_sec = request.user.groups.filter(name='backend').count()
        apertura = JuntaDirectiva.objects.filter(socio=Socio.objects.get(id=request.user.id)).filter(apertura__is_active=True)
        if apertura:
            if request.user.is_authenticated() and is_sec :
                return view_func( request=request,*args, **kwargs )
        else:
            return HttpResponseRedirect(reverse('index'))
    wrap.__doc__ = view_func.__doc__
    wrap.__dict__ = view_func.__dict__
    return wrap

def frontend_login(view_func):
    def wrap(request, *args, **kwargs):
        is_sec = request.user.groups.filter(name='frontend').count()
        if request.user.is_authenticated() and is_sec :
            return view_func( request=request,*args, **kwargs )
        return HttpResponseRedirect(reverse('index'))
    wrap.__doc__ = view_func.__doc__
    wrap.__dict__ = view_func.__dict__
    return wrap