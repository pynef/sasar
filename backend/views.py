from django.shortcuts import render
from django.contrib.auth.models import User,Group
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from legion.decoratos import backend_login,frontend_login
from backend.forms import FormSocio, FormIngreso, FormEgreso, formSocios, FormGaleriaFotos, FormGaleriaFotosEdit, FormSocioVideo, userForm, FormNoticias, FormBanner
from backend.models import Socio,JuntaDirectiva,GaleriaFotos, Noticias, Banner
from backend.models import Apertura, Ingreso, Socio, Egreso, JuntaDirectiva
import time
import os

def home(request):
    usuario = Socio.objects.get(username=request.user.username)
    return render(request,'frontend/index.html')

def desactivo(request):
    usuario = Socio.objects.get(username=request.user.username)
    ctx = {
      'usuario': usuario,
    }
    return render(request,'backend/desactivo.html',ctx)

@backend_login
def temporada(request):
    usuario = Socio.objects.get(username=request.user.username)
    temporada = Apertura.objects.all().order_by('-fin')[0]
    ingresos = Ingreso.objects.filter(socio=usuario)
    try:
        temporada = Apertura.objects.get(is_active=True)
        print "apertura"
        print apertura
        totalI = 0
        for i in ingresos:
            totalI = i.monto+totalI
        el_saldo = temporada.monto_apertura-totalI
    except:
        if request.method == 'POST':
            form = FormSocio(request.POST)
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
        admin = False
        el_saldo = 0
    try:
        admin = usuario.groups.get(name='backend')
    except:
        admin = False
    ctx = {
      'temporada' : temporada,
      'form': form,
      'usuario': usuario,
      'el_saldo': el_saldo,
      'admin': admin,
    }
    return render(request, 'backend/apertura.html', ctx)

@backend_login
def cierre_temporada(request):
    try:
        admin = usuario.groups.get(name='backend')
    except:
        admin = False
    if request.method == 'POST':
        id = request.POST.get('apertura_id')
        print id
        temporada =Apertura.objects.get(id=id)
        temporada.is_active = False
        temporada.save()
    return HttpResponseRedirect(reverse('temporada'))

@backend_login
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

@backend_login
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
    print "endro a backend desde inicios"
    try:
        usuario = Socio.objects.get(username=request.user.username)
        print usuario
        print "usuario"
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
    except:
        cntxt = {
            
            }
        return render(request,'frontend/index.html',cntxt)

@login_required(login_url="/")
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

@login_required(login_url="/")
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

@login_required(login_url="/")
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

@login_required(login_url="/")
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

@login_required(login_url="/")
def borrar_galeria_imagenes(request,id):
    datos = get_object_or_404(GaleriaFotos, pk=id)
    datos.delete()
    return HttpResponseRedirect('/administracion/galeria_imagenes')

@login_required(login_url="/")
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
@login_required(login_url="/")
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
        verdad = True
    else:
        dato = ""
        reportes = ""
        total = 0
        verdad = False
    try:
        admin = usuario.groups.get(name='backend')
    except:
        admin = False
    restante = temporada.monto_apertura - total
    monto_apertura = temporada.monto_apertura
    print temporada.monto_apertura
    cntxt = {
        'dato':dato, 
        'usuario': usuario,
        'socios': socios,
        'reportes': reportes,
        'total': total,
        'el_saldo': el_saldo,
        'admin': admin,
        'restante': restante,
        'monto_apertura': monto_apertura,
        'verdad': verdad,
        }
    return render(request,'backend/reporte_socio.html',cntxt)

@login_required(login_url="/")
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

@login_required(login_url="/")
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

@login_required(login_url="/")
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

@login_required(login_url="/")
def socio_back(request,dni):
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
    return render(request,'backend/socio.html',cntxt)

@backend_login
def nuevo_socio(request):
    usuario = Socio.objects.get(username=request.user.username)
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
    if request.method=='POST':
        formulario = userForm(request.POST)
        print formulario
        if formulario.is_valid():
            personal = formulario.save()
            pwd = request.POST.get('password')
            personal.set_password(pwd)
            personal.is_active = True
            personal.groups.add(3)
            personal.save()
            print pwd
            return HttpResponseRedirect('/administracion/nuevo_socio/')
    else:
        formulario = userForm()
    cntxt = {
        'formulario' : formulario, 'el_saldo': el_saldo, 'admin': admin, 'usuario':usuario
    }
    return render(request, 'backend/nuevo_socio.html', cntxt)

@backend_login
def noticias(request):
    noticias = Noticias.objects.all()
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
        formulario = FormNoticias(request.POST,request.FILES)
        if formulario.is_valid():
            print "se guardo la noticia"
            formulario.save()
            return HttpResponseRedirect('/administracion/noticias')
    else:
        formulario = FormNoticias()
        print formulario
    cntxt = {
        'usuario':usuario, 'el_saldo': el_saldo, 'admin': admin, 'noticias': noticias, 'formulario': formulario,
        }
    return render(request,'backend/noticias.html',cntxt)

@backend_login
def edit_noticias(request,id):
    noticias = Noticias.objects.all()
    noticia = Noticias.objects.get(id=id)
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
        formulario = FormNoticias(request.POST,request.FILES)
        if formulario.is_valid():
            print "se guardo la noticia"
            formulario.save()
            return HttpResponseRedirect('/administracion/noticias')
    else:
        formulario = FormNoticias(instance=noticia)
        print formulario
    cntxt = {
        'usuario':usuario, 'el_saldo': el_saldo, 'admin': admin, 'noticias': noticias, 'formulario': formulario,
        }
    return render(request,'backend/noticias.html',cntxt)

@backend_login
def del_noticias(request,id):
    datos = get_object_or_404(Noticias, pk=id)
    datos.delete()
    return HttpResponseRedirect('/administracion/noticias')

@backend_login
def banner(request):
    banners = Banner.objects.all()
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
        formulario = FormBanner(request.POST,request.FILES)
        if formulario.is_valid():
            print "se guardo la banner"
            formulario.save()
            return HttpResponseRedirect('/administracion/banner')
    else:
        formulario = FormBanner()
        print formulario
    cntxt = {
        'usuario':usuario, 'el_saldo': el_saldo, 'admin': admin, 'banners': banners, 'formulario': formulario,
        }
    return render(request,'backend/banners.html',cntxt)

@backend_login
def edit_banner(request,id):
    banners = Banner.objects.all()
    banner = Banner.objects.get(id=id)
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
        formulario = FormBanner(request.POST,request.FILES)
        if formulario.is_valid():
            print "se guardo la banner"
            formulario.save()
            return HttpResponseRedirect('/administracion/banner')
    else:
        formulario = FormBanner(instance=banner)
        print formulario
    cntxt = {
        'usuario':usuario, 'el_saldo': el_saldo, 'admin': admin, 'banners': banners, 'formulario': formulario,
        }
    return render(request,'backend/banners.html',cntxt)

@backend_login
def del_banner(request,id):
    datos = get_object_or_404(Banner, pk=id)
    datos.delete()
    return HttpResponseRedirect('/administracion/banner')