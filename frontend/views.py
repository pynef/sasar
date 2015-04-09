# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.models import User,Group
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from legion.decoratos import backend_login,frontend_login
from backend.models import Socio, GaleriaFotos, Ingreso, Apertura, Noticias, Banner

def inicio(request):
    noti = Banner.objects.all().order_by('-id')[:1].get()
    print "notficacion"
    print noti
    print "notficacion"
    cntxt={
        'noti':noti,
    }
    return render(request,'frontend/index.html',cntxt)

def home(request):
    noti = Banner.objects.all().order_by('-id')[:1]
    print "notficacion"
    print noti
    print "notficacion"
    cntxt={
        'noti':noti,
    }
    return render(request,'frontend/index.html',cntxt)

def responsabilidad_social(request):
    return render(request,'frontend/responsabilidad_social.html')

def quienes_somos(request):
    return render(request,'frontend/quienes_somos.html')

def reglamentos(request):
    return render(request,'frontend/reglamentos.html')

def estatutos(request):
    return render(request,'frontend/estatutos.html')

def informes(request):
    return render(request,'frontend/informes.html')

def periodismo(request):
    return render(request,'frontend/periodismo.html')


def socios(request):
    usuarios = Socio.objects.all()
    print usuarios
    cntxt={
        'usuarios':usuarios,
    }
    return render(request,'frontend/socios.html',cntxt)

def las_noticias(request):
    las_noticias = Noticias.objects.all()
    print las_noticias
    cntxt={
        'las_noticias':las_noticias,
    }
    return render(request,'frontend/las_noticias.html',cntxt)

def socio(request,dni):
    socio = Socio.objects.get(dni=dni)
    galeria_imagenes = GaleriaFotos.objects.filter(socio=Socio.objects.get(dni=dni))
    cntxt={
        'socio':socio, 'galeria_imagenes': galeria_imagenes,
    }
    return render(request,'frontend/socio.html',cntxt)

def index(request):
    if request.user.is_authenticated() :
        print "logeado"
        print request.user.is_active
        if request.user.groups.filter(name='backend'):
            return HttpResponseRedirect('/administracion/')
        elif request.user.groups.filter(name='frontend'):
            return HttpResponseRedirect('/home/')
        else:
            return HttpResponseRedirect('/logout')
            print "salir no usuario"
    else:
        print "no logeado"
        return HttpResponseRedirect('/home/')