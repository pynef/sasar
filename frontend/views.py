# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.models import User,Group
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from legion.decoratos import backend_login,frontend_login
from backend.models import Socio, GaleriaFotos, Ingreso, Apertura

def inicio(request):
    return render(request,'frontend/index.html')

def home(request):
    return render(request,'frontend/index.html')

def nosotros(request):
    usuarios = Socio.objects.all()
    print usuarios
    cntxt={
        'usuarios':usuarios,
    }
    return render(request,'frontend/nosotros.html',cntxt)

def socio(request,dni):
    usuario = Socio.objects.get(username=request.user.username)
    socio = Socio.objects.get(dni=dni)
    galeria_imagenes = GaleriaFotos.objects.filter(socio=Socio.objects.get(dni=dni))
    ingresoSocio = Ingreso.objects.filter(socio=usuario)
    temporada = Apertura.objects.get(is_active=True)
    totalI = 0
    for i in ingresoSocio:
        totalI = i.monto+totalI
    el_saldo = temporada.monto_apertura-totalI
    try:
        admin = usuario.groups.get(name='backend')
    except:
        admin = False
    cntxt={
        'usuario':usuario,'socio':socio, 'galeria_imagenes': galeria_imagenes, 'el_saldo': el_saldo, 'admin': admin,
    }
    return render(request,'frontend/socio.html',cntxt)

def index(request):
    if request.user.is_authenticated() :
        print "logeado"
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