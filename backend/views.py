from django.shortcuts import render
from django.contrib.auth.models import User,Group
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from legion.decoratos import backend_login,frontend_login
from backend.forms import FormSocio, FormIngreso, FormEgreso, formSocios, FormGaleriaFotos, FormGaleriaFotosEdit, FormSocioVideo
from backend.models import Socio,JuntaDirectiva,GaleriaFotos
from backend.models import Apertura, Ingreso, Socio, Egreso, JuntaDirectiva
import time
import os

def home(request):
    usuario = Socio.objects.get(username=req.user.username)
    return render(request,'frontend/index.html')

def temporada(req):
    usuario = Socio.objects.get(username=req.user.username)
    temporada = Apertura.objects.all().order_by('-fin')[0]
    ingresos = Ingreso.objects.filter(socio=usuario)
    temporada = Apertura.objects.get(is_active=True)
    totalI = 0
    for i in ingresos:
        totalI = i.monto+totalI
    el_saldo = temporada.monto_apertura-totalI
    try:
        admin = usuario.groups.get(name='backend')
    except:
        admin = False
    if req.method == 'POST':
        form = FormSocio(req.POST)
        form.saldo_anterior = temporada.saldo_anterior
        if form.is_valid():
            nueva_temporada = form.save()
            nueva_temporada.saldo_anterior = temporada.saldo
            nueva_temporada.save()
            temporada = nueva_temporada
        else:
            pass
    else:
        form = FormSocio()
    ctx = {
      'temporada' : temporada,
      'form': form,
      'usuario': usuario,
      'el_saldo': el_saldo,
      'admin': admin,
    }
    return render(req, 'backend/apertura.html', ctx)

def cierre_temporada(req):
    if req.method == 'POST':
        id = req.POST.get('apertura_id')
        print id
        temporada =Apertura.objects.get(id=id)
        temporada.is_active = False
        temporada.save()
    return HttpResponseRedirect(reverse('temporada'))

def ingreso(req):
    usuario = Socio.objects.get(username=req.user.username)
    apertura = Apertura.objects.get(is_active=True)
    socios = Socio.objects.all()
    ultimos_pagos = Ingreso.objects.all().order_by('-create_at')[:4]
    ingresos = Ingreso.objects.filter(socio=usuario)
    temporada = Apertura.objects.get(is_active=True)
    totalI = 0
    for i in ingresos:
        totalI = i.monto+totalI
    el_saldo = temporada.monto_apertura-totalI
    try:
        admin = usuario.groups.get(name='backend')
    except:
        admin = False
    if req.method == 'POST':
        formulario = FormIngreso(req.POST)
        if formulario.is_valid():
            ingreso=formulario.save()
        else:
            print formulario
    else:
        formulario = FormIngreso()
    ctx = {
        'formulario' : formulario, 'apertura' : apertura, 'ultimos_pagos': ultimos_pagos, 'socios': socios, 'usuario': usuario, 'el_saldo': el_saldo, 'admin': admin,
    }
    return render(req, 'backend/ingresos.html',ctx)

def egresos(req):
    apertura = Apertura.objects.get(is_active=True)
    usuario = Socio.objects.get(username=req.user.username)
    ultimos_pagos = Egreso.objects.all().order_by('-create_at')[:5]
    ingresos = Ingreso.objects.filter(socio=usuario)
    temporada = Apertura.objects.get(is_active=True)
    totalI = 0
    for i in ingresos:
        totalI = i.monto+totalI
    el_saldo = temporada.monto_apertura-totalI
    try:
        admin = usuario.groups.get(name='backend')
    except:
        admin = False
    if req.method == 'POST':
        formulario = FormEgreso(req.POST)
        if formulario.is_valid():
            ingreso=formulario.save()
        else:
            print formulario
    else:
        formulario = FormEgreso()
    ctx = {
        'formulario' : formulario, 'apertura' : apertura, 'ultimos_pagos': ultimos_pagos, 'usuario': usuario, 'el_saldo':el_saldo, 'admin': admin,
    }
    return render(req, 'backend/egresos.html',ctx)

def index(request):
    usuario = Socio.objects.get(username=request.user.username)
    ingresos = Ingreso.objects.filter(socio=usuario)
    temporada = Apertura.objects.get(is_active=True)
    totalI = 0
    for i in ingresos:
        totalI = i.monto+totalI
    el_saldo = temporada.monto_apertura-totalI
    try:
        admin = usuario.groups.get(name='backend')
    except:
        admin = False
    cntxt = {
        'usuario':usuario, 'el_saldo': el_saldo, 'admin': admin
        }
    return render(request,'backend/index.html',cntxt)


def perfil(request):
    usuario = Socio.objects.get(username=request.user.username)
    ingresos = Ingreso.objects.filter(socio=usuario)
    temporada = Apertura.objects.get(is_active=True)
    totalI = 0
    for i in ingresos:
        totalI = i.monto+totalI
    el_saldo = temporada.monto_apertura-totalI
    try:
        admin = usuario.groups.get(name='backend')
    except:
        admin = False
    if request.method == 'POST':
    	formulario = formSocios(request.POST,request.FILES,instance=usuario)
    	if formulario.is_valid():
    		formulario.save()
    		return HttpResponseRedirect('/administracion')
    else:
    	formulario = formSocios(instance=usuario)
    cntxt = {
    'usuario':usuario,'formulario':formulario, 'el_saldo': el_saldo, 'admin': admin,
    }
    return render (request,'backend/profile.html',cntxt)

def galeria_video(request):
    usuario = Socio.objects.get(username=request.user.username)
    try:
        admin = usuario.groups.get(name='backend')
    except:
        admin = False
    ingresos = Ingreso.objects.filter(socio=usuario)
    temporada = Apertura.objects.get(is_active=True)
    totalI = 0
    for i in ingresos:
        totalI = i.monto+totalI
    el_saldo = temporada.monto_apertura-totalI
    if request.method == 'POST':
        formulario = FormSocioVideo(request.POST,request.FILES,instance=usuario)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/administracion')
    else:
        formulario = FormSocioVideo(instance=usuario)
    cntxt = {
    'usuario':usuario,'formulario':formulario, 'el_saldo': el_saldo, 'admin': admin,
    }
    return render (request,'backend/galeria_video.html',cntxt)

def galeria_imagenes(request):
    usuario = Socio.objects.get(username=request.user.username)
    imagenes = GaleriaFotos.objects.filter(socio=Socio.objects.get(username=request.user.username)).order_by('-id')
    ingresos = Ingreso.objects.filter(socio=usuario)
    temporada = Apertura.objects.get(is_active=True)
    totalI = 0
    try:
        admin = usuario.groups.get(name='backend')
    except:
        admin = False
    for i in ingresos:
        totalI = i.monto+totalI
    el_saldo = temporada.monto_apertura-totalI
    if request.method == 'POST':
        formulario = FormGaleriaFotos(request.POST,request.FILES)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/administracion/galeria_imagenes')
    else:
        formulario = FormGaleriaFotos()
    cntxt = {
        'imagenes':imagenes, 'formulario':formulario, 'usuario': usuario, 'el_saldo': el_saldo, 'admin': admin,
        }
    return render(request,'backend/galeria_imagenes.html',cntxt)

def edit_galeria_imagenes(request,id):
    usuario = Socio.objects.get(username=request.user.username)
    imagenes = GaleriaFotos.objects.filter(socio=Socio.objects.get(username=request.user.username)).order_by('-id')
    imagen = GaleriaFotos.objects.get(id=id)
    ingresos = Ingreso.objects.filter(socio=usuario)
    temporada = Apertura.objects.get(is_active=True)
    totalI = 0
    for i in ingresos:
        totalI = i.monto+totalI
    el_saldo = temporada.monto_apertura-totalI
    try:
        admin = usuario.groups.get(name='backend')
    except:
        admin = False
    if request.method == 'POST':
        formulario = FormGaleriaFotosEdit(request.POST,request.FILES,instance=imagen)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/administracion/galeria_imagenes')
    else:
        formulario = FormGaleriaFotosEdit(instance=imagen)
    cntxt = {
    'usuario':usuario,'imagenes':imagenes,'formulario':formulario, 'el_saldo': el_saldo, 'admin': admin,
    }
    return render (request,'backend/edit_galeria_imagenes.html',cntxt)

def borrar_galeria_imagenes(request,id):
    datos = get_object_or_404(GaleriaFotos, pk=id)
    datos.delete()
    return HttpResponseRedirect('/administracion/galeria_imagenes')

def junta_directiva(request):
    usuario = Socio.objects.get(username=request.user.username)
    junta_directiva = JuntaDirectiva.objects.filter(apertura__is_active=True)
    ingresos = Ingreso.objects.filter(socio=usuario)
    temporada = Apertura.objects.get(is_active=True)
    totalI = 0
    for i in ingresos:
        totalI = i.monto+totalI
    el_saldo = temporada.monto_apertura-totalI
    try:
        admin = usuario.groups.get(name='backend')
    except:
        admin = False
    cntxt = {
        'junta_directiva':junta_directiva, 'usuario': usuario, 'el_saldo': el_saldo, 'admin': admin,
        }
    return render(request,'backend/junta_directiva.html',cntxt)


# def password_reset(request):
#     usuario = Socio.objects.get(username=request.user.username)
#     cntxt = {
#         'usuario': usuario,
#         }
#     return render(request,'registration/password_reset.html',cntxt)


# REPORTES
def reporte_socio(request):
    usuario = Socio.objects.get(username=request.user.username)
    socios = Socio.objects.all()
    ingresos = Ingreso.objects.filter(socio=usuario)
    temporada = Apertura.objects.get(is_active=True)
    totalI = 0
    for i in ingresos:
        totalI = i.monto+totalI
    el_saldo = temporada.monto_apertura-totalI
    if request.method == 'POST':
        dato = request.POST.get("socio")
        reportes = Ingreso.objects.filter(socio=Socio.objects.get(id=dato))
        total = 0
        for i in reportes:
            total = i.monto + total
    else:
        dato = ""
        reportes = ""
        total = 0
    try:
        admin = usuario.groups.get(name='backend')
    except:
        admin = False
    cntxt = {
        'dato':dato, 'usuario': usuario, 'socios': socios, 'reportes': reportes, 'total': total, 'el_saldo': el_saldo, 'admin': admin,
        }
    return render(request,'backend/reporte_socio.html',cntxt)

def reporte_ingresos(request):
    usuario = Socio.objects.get(username=request.user.username)
    ingresos = Ingreso.objects.all().order_by('-id')
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
    cntxt = {
        'usuario': usuario, 'ingresos': ingresos, 'el_saldo': el_saldo, 'admin': admin,
        }
    return render(request,'backend/reporte_ingresos.html',cntxt)

def reporte_egresos(request):
    usuario = Socio.objects.get(username=request.user.username)
    egresos = Egreso.objects.all().order_by('-id')
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
    cntxt = {
        'usuario': usuario, 'egresos': egresos, 'el_saldo': el_saldo, 'admin': admin,
        }
    return render(request,'backend/reporte_egresos.html',cntxt)

def reporte_general(request):
    usuario = Socio.objects.get(username=request.user.username)
    egresos = Egreso.objects.all().order_by('-id')
    ingresos = Ingreso.objects.all().order_by('-id')
    total_egresos = 0
    total_ingresos = 0
    for i in egresos:
        total_egresos = i.monto+total_egresos
    for i in ingresos:
        total_ingresos = i.monto+total_ingresos
    saldo = total_ingresos-total_egresos
    try:
        admin = usuario.groups.get(name='backend')
    except:
        admin = False
    hoy = time.strftime('%d/%m/%y')
    ingresoSocio = Ingreso.objects.filter(socio=usuario)
    temporada = Apertura.objects.get(is_active=True)
    totalI = 0
    for i in ingresoSocio:
        totalI = i.monto+totalI
    el_saldo = temporada.monto_apertura-totalI

    cntxt = {
        'usuario': usuario, 'total_ingresos': total_ingresos,'total_egresos': total_egresos, 'saldo':saldo, 'hoy': hoy, 'el_saldo': el_saldo, 'admin': admin,
        }
    return render(request,'backend/reporte_general.html',cntxt)