# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.models import User,Group
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from legion.decoratos import administrador_login,backend_login,frontend_login
from backend.models import Socio

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
    usuario = Socio.objects.get(dni=dni)
    print usuario.first_name
    cntxt={
        'usuario':usuario,
    }
    return render(request,'frontend/socio.html',cntxt)

def index(request):
    if request.user.is_authenticated() :
        print "logeado"
        if request.user.groups.filter(name='administracion'):
            return HttpResponseRedirect('/administrador/')
        elif request.user.groups.filter(name='backend'):
            return HttpResponseRedirect('/panel/')
        elif request.user.groups.filter(name='frontend'):
            return HttpResponseRedirect('/home/')
        else:
            return HttpResponseRedirect('/logout')
            print "salir no usuario"
    else:
        print "no logeado"
        return HttpResponseRedirect('/home/')