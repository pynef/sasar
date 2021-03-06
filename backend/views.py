from django.shortcuts import render
from django.contrib.auth.models import User,Group
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from legion.decoratos import backend_login,frontend_login, apertura_activa, presidente, apertura_inactiva
from backend.forms import FormSocio, FormIngreso, FormEgreso, formSocios, FormGaleriaFotos, FormGaleriaFotosEdit, FormSocioVideo, userForm, FormNoticias, FormBanner, FormFotos, FormJuntaDirectiva, FormResponsabilidadSocial, FormPortadas, FormVideoPortada
from backend.models import Socio,JuntaDirectiva,GaleriaFotos, Noticias, Banner, Fotos, ResponsabilidadSocial, Portadas
from backend.models import Apertura, Ingreso, Socio, Egreso, JuntaDirectiva, Categoria, Cargo, VideoPortada
import time
import os

@backend_login
@apertura_activa
def homes(request):
    usuario = Socio.objects.get(username=request.user.username)
    print "homes"
    print apertura_activa
    print "homes"
    return render(request,'frontend/index.html')

def desactivo(request):
    usuario = Socio.objects.get(username=request.user.username)
    ctx = {
      'usuario': usuario,
    }
    return render(request,'backend/desactivo.html',ctx)


@backend_login
def temporada(request):
    socios = Socio.objects.all()
    cargos = Cargo.objects.all()
    usuario = Socio.objects.get(username=request.user.username)
    temporada = Apertura.objects.all().order_by('-id')[0]
    ingresos = Ingreso.objects.filter(socio=usuario)
    try:
        temporadas = Apertura.objects.get(is_active=True)
        totalI = 0
        for i in ingresos:
            totalI = i.monto+totalI
        el_saldo = temporadas.monto_apertura-totalI
    except:
        admin = False
        el_saldo = 0
    try:
        admin = JuntaDirectiva.objects.filter(socio=Socio.objects.get(id=usuario.id)).filter(apertura__is_active=True)
    except:
        admin = False
    ctx = {
      'temporada' : temporada,
      'usuario': usuario,
      'el_saldo': el_saldo,
      'admin': admin,
    }
    return render(request, 'backend/apertura.html', ctx)

@apertura_inactiva
def apertura_inactiva(request):
    socios = Socio.objects.all()
    cargos = Cargo.objects.all()
    usuario = Socio.objects.get(username=request.user.username)
    temporada = Apertura.objects.all().order_by('-id')[0]
    ingresos = Ingreso.objects.filter(socio=usuario)
    try:
        temporadas = Apertura.objects.get(is_active=True)
        print "apertura"
        print apertura
        totalI = 0
        for i in ingresos:
            totalI = i.monto+totalI
        el_saldo = temporadas.monto_apertura-totalI
    except:
        if request.method == 'POST':
            form = FormSocio(request.POST)
            form.saldo_anterior = temporada.saldo_anterior
            if form.is_valid():
                idsocio = request.POST.get('socio')
                nueva_temporada = form.save()
                nueva_temporada.user = usuario
                nueva_temporada.saldo_anterior = temporada.saldo
                nueva_temporada.save()
                temporada = nueva_temporada

                junta = JuntaDirectiva.objects.create(
                    socio = Socio.objects.get(id=idsocio),
                    apertura = nueva_temporada,
                    cargo = Cargo.objects.get(id=1)
                    )
                junta.save()

                grupo = Group.objects.get(name="backend")
                soc = Socio.objects.get(id=idsocio)
                soc.groups.add(grupo)
                soc.save()
                return HttpResponseRedirect(reverse('temporada'))
            else:
                print form
                pass
        else:
            form = FormSocio()
        admin = False
        el_saldo = 0
    try:
        admin = JuntaDirectiva.objects.filter(socio=Socio.objects.get(id=usuario.id)).filter(apertura__is_active=True)
    except:
        admin = False
    ctx = {
      'cargos' : cargos,
      'socios' : socios,
      'temporada' : temporada,
      'form': form,
      'usuario': usuario,
      'el_saldo': el_saldo,
      'admin': admin,
    }
    return render(request, 'backend/apertura_inactiva.html', ctx)

@backend_login
def cierre_temporada(request):
    try:
        admin = JuntaDirectiva.objects.filter(socio=Socio.objects.get(id=usuario.id)).filter(apertura__is_active=True)
    except:
        admin = False
    if request.method == 'POST':
        id = request.POST.get('apertura_id')
        print id
        temporada =Apertura.objects.get(id=id)
        temporada.is_active = False
        temporada.save()
    return HttpResponseRedirect(reverse('temporada'))

@apertura_activa
@backend_login
def ingreso(request):
    usuario = Socio.objects.get(username=request.user.username)
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
        admin = JuntaDirectiva.objects.filter(socio=Socio.objects.get(id=usuario.id)).filter(apertura__is_active=True)
    except:
        admin = False
    if request.method == 'POST':
        formulario = FormIngreso(request.POST)
        if formulario.is_valid():
            ingreso=formulario.save()
            return HttpResponseRedirect(reverse('ingreso'))
        else:
            print formulario
    else:
        formulario = FormIngreso()
    ctx = {
        'formulario' : formulario, 'apertura' : apertura, 'ultimos_pagos': ultimos_pagos, 'socios': socios, 'usuario': usuario, 'el_saldo': el_saldo, 'admin': admin,
    }
    return render(request, 'backend/ingresos.html',ctx)


@apertura_activa
def egresos(request):
    apertura = Apertura.objects.get(is_active=True)
    usuario = Socio.objects.get(username=request.user.username)
    ultimos_pagos = Egreso.objects.all().order_by('-create_at')[:5]
    ingresos = Ingreso.objects.filter(socio=usuario)
    temporada = Apertura.objects.get(is_active=True)
    totalI = 0
    for i in ingresos:
        totalI = i.monto+totalI
    el_saldo = temporada.monto_apertura-totalI
    try:
        admin = JuntaDirectiva.objects.filter(socio=Socio.objects.get(id=usuario.id)).filter(apertura__is_active=True)
    except:
        admin = False
    if request.method == 'POST':
        formulario = FormEgreso(request.POST)
        if formulario.is_valid():
            ingreso=formulario.save()
            return HttpResponseRedirect(reverse('egresos'))
        else:
            print formulario
    else:
        formulario = FormEgreso()
    ctx = {
        'formulario' : formulario, 'apertura' : apertura, 'ultimos_pagos': ultimos_pagos, 'usuario': usuario, 'el_saldo':el_saldo, 'admin': admin,
    }
    return render(request, 'backend/egresos.html',ctx)

@apertura_activa
@login_required(login_url="/")
def index(request):
    print "endro a backend desde inicios"
    usuario = Socio.objects.get(username=request.user.username)
    print usuario
    print "usuario"
    temporada = Apertura.objects.get(is_active=True)
    ingresos = Ingreso.objects.filter(socio=usuario)
    totalI = 0
    for i in ingresos:
        totalI = i.monto+totalI
    el_saldo = temporada.monto_apertura-totalI
    try:
        admin = JuntaDirectiva.objects.filter(socio=Socio.objects.get(id=usuario.id)).filter(apertura__is_active=True)
    except:
        admin = False
    cntxt = {
        'usuario':usuario, 'el_saldo': el_saldo, 'admin': admin
        }
    return render(request,'backend/index.html',cntxt)

@login_required(login_url="/")
@apertura_activa
def perfil(request):
    try:
        temporada = Apertura.objects.get(is_active=True)
        usuario = Socio.objects.get(username=request.user.username)
        ingresos = Ingreso.objects.filter(socio=usuario)
        totalI = 0
        for i in ingresos:
            totalI = i.monto+totalI
        el_saldo = temporada.monto_apertura-totalI
        try:
            admin = JuntaDirectiva.objects.filter(socio=Socio.objects.get(id=usuario.id)).filter(apertura__is_active=True)
        except:
            admin = False
        if request.method == 'POST':
        	formulario = formSocios(request.POST,request.FILES,instance=usuario)
        	if formulario.is_valid():
        		formulario.save()
        		return HttpResponseRedirect('/administracion')
        else:
        	formulario = formSocios(instance=usuario)
    except:
        return render(request,'frontend/quienes_somos.html')
    cntxt = {
    'usuario':usuario,'formulario':formulario, 'el_saldo': el_saldo, 'admin': admin,
    }
    return render (request,'backend/profile.html',cntxt)

@login_required(login_url="/")
@apertura_activa
def galeria_video(request):
    usuario = Socio.objects.get(username=request.user.username)
    try:
        admin = JuntaDirectiva.objects.filter(socio=Socio.objects.get(id=usuario.id)).filter(apertura__is_active=True)
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
            return HttpResponseRedirect(reverse('galeria_video'))
        else:
            print formulario
    else:
        formulario = FormSocioVideo(instance=usuario)
    cntxt = {
    'usuario':usuario,'formulario':formulario, 'el_saldo': el_saldo, 'admin': admin,
    }
    return render (request,'backend/galeria_video.html',cntxt)

@login_required(login_url="/")
@apertura_activa
def galeria_imagenes(request):
    usuario = Socio.objects.get(username=request.user.username)
    imagenes = GaleriaFotos.objects.filter(socio=Socio.objects.get(username=request.user.username)).order_by('-id')
    ingresos = Ingreso.objects.filter(socio=usuario)
    temporada = Apertura.objects.get(is_active=True)
    totalI = 0
    try:
        admin = JuntaDirectiva.objects.filter(socio=Socio.objects.get(id=usuario.id)).filter(apertura__is_active=True)
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
@apertura_activa
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
        admin = JuntaDirectiva.objects.filter(socio=Socio.objects.get(id=usuario.id)).filter(apertura__is_active=True)
    except:
        admin = False
    if request.method == 'POST':
        formulario = FormGaleriaFotosEdit(request.POST,request.FILES,instance=imagen)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/administracion/galeria_imagenes')
        else:
            print formulario
    else:
        formulario = FormGaleriaFotosEdit(instance=imagen)
    cntxt = {
    'usuario':usuario,'imagen':imagen,'imagenes':imagenes,'formulario':formulario, 'el_saldo': el_saldo, 'admin': admin,
    }
    return render (request,'backend/edit_galeria_imagenes.html',cntxt)

@login_required(login_url="/")
@apertura_activa
def borrar_galeria_imagenes(request,id):
    datos = get_object_or_404(GaleriaFotos, pk=id)
    datos.delete()
    return HttpResponseRedirect('/administracion/galeria_imagenes')

@login_required(login_url="/")
@apertura_activa
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
        admin = JuntaDirectiva.objects.filter(socio=Socio.objects.get(id=usuario.id)).filter(apertura__is_active=True)
    except:
        admin = False
    cntxt = {
        'junta_directiva':junta_directiva, 'usuario': usuario, 'el_saldo': el_saldo, 'admin': admin,
        }
    return render(request,'backend/junta_directiva.html',cntxt)

@backend_login
@apertura_activa
def nueva_junta_directiva(request):
    usuario = Socio.objects.get(username=request.user.username)
    cargos = Cargo.objects.all()
    socios = Socio.objects.all()
    juntas = JuntaDirectiva.objects.filter(apertura__is_active=True)
    ingresos = Ingreso.objects.filter(socio=usuario)
    temporada = Apertura.objects.get(is_active=True)
    totalI = 0
    for i in ingresos:
        totalI = i.monto+totalI
    el_saldo = temporada.monto_apertura-totalI
    try:
        print "usuario"
        print usuario
        admin = JuntaDirectiva.objects.filter(socio=Socio.objects.get(id=usuario.id)).filter(apertura__is_active=True)
        print admin
        print "administrador"
    except:
        admin = False
    if request.method=='POST':
        formulario = FormJuntaDirectiva(request.POST)
        grupo = Group.objects.get(name="backend")
        miembro_sasar = request.POST.get("socio")
        miembro_nuevo = Socio.objects.get(id=miembro_sasar)
        miembro_nuevo.groups.add(grupo)
        print miembro_nuevo
        if formulario.is_valid():
            junta = formulario.save()
            # junta.groups.add(grupo)
            junta.save()
            return HttpResponseRedirect('/administracion/nueva_junta_directiva/')
    else:
        formulario = FormJuntaDirectiva()
    cntxt = {
        'temporada': temporada,
        'juntas':juntas,
         'usuario': usuario, 
         'el_saldo': el_saldo, 
         'admin': admin, 
         'formulario': formulario,
         'cargos': cargos,
         'socios': socios,
        }
    return render(request,'backend/nueva_junta_directiva.html',cntxt)

@apertura_activa
def edit_junta_directiva(request, id):
    miembro_junta = JuntaDirectiva.objects.get(id=id)
    usuario = Socio.objects.get(username=request.user.username)
    cargos = Cargo.objects.all()
    socios = Socio.objects.all()
    juntas = JuntaDirectiva.objects.filter(apertura__is_active=True)
    ingresos = Ingreso.objects.filter(socio=usuario)
    temporada = Apertura.objects.get(is_active=True)
    totalI = 0
    for i in ingresos:
        totalI = i.monto+totalI
    el_saldo = temporada.monto_apertura-totalI
    try:
        admin = JuntaDirectiva.objects.filter(socio=Socio.objects.get(id=usuario.id)).filter(apertura__is_active=True)
    except:
        admin = False
    if request.method=='POST':
        formulario = FormJuntaDirectiva(request.POST,request.FILES,instance=miembro_junta)
        print formulario
        if formulario.is_valid():
            junta = formulario.save()
            junta.save()
            return HttpResponseRedirect('/administracion/nueva_junta_directiva/')
    else:
        formulario = FormJuntaDirectiva()
    cntxt = {
        'temporada': temporada,
        'juntas':juntas,
         'usuario': usuario, 
         'el_saldo': el_saldo, 
         'admin': admin, 
         'formulario': formulario,
         'cargos': cargos,
         'socios': socios,
        }
    return render(request,'backend/edit_junta_directiva.html',cntxt)

@apertura_activa
def borrar_junta_directiva(request,id):
    datos = get_object_or_404(JuntaDirectiva, pk=id)
    socio = datos.socio
    grupo = Group.objects.get(name='backend')
    socio.groups.remove(grupo)
    print "datos para borrar"
    print datos
    datos.delete()
    return HttpResponseRedirect('/administracion/nueva_junta_directiva')
# def password_reset(request):
#     usuario = Socio.objects.get(username=request.user.username)
#     cntxt = {
#         'usuario': usuario,
#         }
#     return render(request,'registration/password_reset.html',cntxt)


# REPORTES
@login_required(login_url="/")
@apertura_activa
def reporte_socio(request):
    usuario = Socio.objects.get(username=request.user.username)
    socios = Socio.objects.all()
    temporadas_totales = Apertura.objects.all()
    ingresos = Ingreso.objects.filter(socio=usuario)
    temporada = Apertura.objects.get(is_active=True)
    totalI = 0
    for i in ingresos:
        totalI = i.monto+totalI
    el_saldo = temporada.monto_apertura-totalI
    if request.method == 'POST':
        dato = request.POST.get("socio")
        apert = request.POST.get("apertura")
        reportes = Ingreso.objects.filter(socio=Socio.objects.get(id=dato)).filter(apertura=Apertura.objects.get(id=apert))
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
        admin = JuntaDirectiva.objects.filter(socio=Socio.objects.get(id=usuario.id)).filter(apertura__is_active=True)
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
        'temporadas_totales': temporadas_totales,
        }
    return render(request,'backend/reporte_socio.html',cntxt)

@login_required(login_url="/")
@apertura_activa
def reporte_ingresos(request):
    temporadas = Apertura.objects.all()
    usuario = Socio.objects.get(username=request.user.username)
    ingresoSocio = Ingreso.objects.filter(socio=usuario)
    temporada = Apertura.objects.get(is_active=True)
    totalI = 0
    for i in ingresoSocio:
        totalI = i.monto+totalI
    el_saldo = temporada.monto_apertura-totalI
    try:
        admin = JuntaDirectiva.objects.filter(socio=Socio.objects.get(id=usuario.id)).filter(apertura__is_active=True)
    except:
        admin = False
    if request.method == 'POST':
        apert = request.POST.get("apertura")
        ingresos = Ingreso.objects.filter(apertura=Apertura.objects.get(id=apert)).order_by('-id')
    else:
        ingresos = []
    cntxt = {
        'usuario': usuario, 'ingresos': ingresos, 'el_saldo': el_saldo, 'admin': admin,'temporadas': temporadas,
        }
    return render(request,'backend/reporte_ingresos.html',cntxt)

@login_required(login_url="/")
@apertura_activa
def reporte_egresos(request):
    temporadas = Apertura.objects.all()
    usuario = Socio.objects.get(username=request.user.username)
    ingresoSocio = Ingreso.objects.filter(socio=usuario)
    temporada = Apertura.objects.get(is_active=True)
    totalI = 0
    for i in ingresoSocio:
        totalI = i.monto+totalI
    el_saldo = temporada.monto_apertura-totalI
    try:
        admin = JuntaDirectiva.objects.filter(socio=Socio.objects.get(id=usuario.id)).filter(apertura__is_active=True)
    except:
        admin = False
    if request.method == 'POST':
        apert = request.POST.get("apertura")
        egresos = Egreso.objects.filter(apertura=Apertura.objects.get(id=apert)).order_by('-id')
    else:
        egresos = []
    cntxt = {
        'usuario': usuario, 'egresos': egresos, 'el_saldo': el_saldo, 'admin': admin,'temporadas': temporadas,
        }
    return render(request,'backend/reporte_egresos.html',cntxt)

@login_required(login_url="/")
@apertura_activa
def reporte_general(request):
    temporadas = Apertura.objects.all()
    print temporadas
    usuario = Socio.objects.get(username=request.user.username)
    try:
        admin = JuntaDirectiva.objects.filter(socio=Socio.objects.get(id=usuario.id)).filter(apertura__is_active=True)
    except:
        admin = False

    ingresoSocio = Ingreso.objects.filter(socio=usuario)
    temporada = Apertura.objects.get(is_active=True)
    totalI = 0
    for i in ingresoSocio:
        totalI = i.monto+totalI
    el_saldo = temporada.monto_apertura-totalI

    if request.method == 'POST':
        apert = request.POST.get("apertura")
        egresos = Egreso.objects.filter(apertura=Apertura.objects.get(id=apert)).order_by('-id')
        ingresos = Ingreso.objects.filter(apertura=Apertura.objects.get(id=apert)).order_by('-id')
        total_egresos = 0
        total_ingresos = 0
        for i in egresos:
            total_egresos = i.monto+total_egresos
        for i in ingresos:
            total_ingresos = i.monto+total_ingresos
        saldo = total_ingresos-total_egresos
    else:
        total_ingresos = 0
        total_egresos = 0
        saldo = 0
    hoy = time.strftime('%d/%m/%y')
    

    cntxt = {
        'usuario': usuario,
        'total_ingresos': total_ingresos,
        'total_egresos': total_egresos,
        'saldo':saldo,
        'hoy': hoy,
        'el_saldo': el_saldo,
        'admin': admin,
        'temporadas': temporadas,
        }
    return render(request,'backend/reporte_general.html',cntxt)

@login_required(login_url="/")
@apertura_activa
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
        admin = JuntaDirectiva.objects.filter(socio=Socio.objects.get(id=usuario.id)).filter(apertura__is_active=True)
    except:
        admin = False
    cntxt={
        'usuario':usuario,'socio':socio, 'galeria_imagenes': galeria_imagenes, 'el_saldo': el_saldo, 'admin': admin,
    }
    return render(request,'backend/socio.html',cntxt)

@backend_login
@apertura_activa
def nuevo_socio(request):
    mensaje = ""
    usuario = Socio.objects.get(username=request.user.username)
    ingresoSocio = Ingreso.objects.filter(socio=usuario)
    temporada = Apertura.objects.get(is_active=True)
    totalI = 0
    for i in ingresoSocio:
        totalI = i.monto+totalI
    el_saldo = temporada.monto_apertura-totalI
    try:
        admin = JuntaDirectiva.objects.filter(socio=Socio.objects.get(id=usuario.id)).filter(apertura__is_active=True)
    except:
        admin = False
    if request.method=='POST':
        formulario = userForm(request.POST)
        if formulario.is_valid():
            personal = formulario.save()
            mensaje = "El Usuario " +personal.username + " Fue Registrado"
            pwd = request.POST.get('password')
            personal.set_password(pwd)
            personal.is_active = True
            personal.groups.add(3)
            personal.save()
            formulario = userForm()
            # return HttpResponseRedirect('/administracion/nuevo_socio/')
        else:
            print formulario.errors
            formulario = userForm()
            mensaje = ""
    else:
        formulario = userForm()
    cntxt = {
        'formulario' : formulario, 'el_saldo': el_saldo, 'admin': admin, 'usuario':usuario,
        'mensaje':mensaje,
    }
    return render(request, 'backend/nuevo_socio.html', cntxt)

@backend_login
@apertura_activa
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
        admin = JuntaDirectiva.objects.filter(socio=Socio.objects.get(id=usuario.id)).filter(apertura__is_active=True)
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
@apertura_activa
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
        admin = JuntaDirectiva.objects.filter(socio=Socio.objects.get(id=usuario.id)).filter(apertura__is_active=True)
    except:
        admin = False
    if request.method == 'POST':
        formulario = FormNoticias(request.POST,request.FILES,instance=noticia)
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
@apertura_activa
def del_noticias(request,id):
    datos = get_object_or_404(Noticias, pk=id)
    datos.delete()
    return HttpResponseRedirect('/administracion/noticias')

@backend_login
@apertura_activa
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
        admin = JuntaDirectiva.objects.filter(socio=Socio.objects.get(id=usuario.id)).filter(apertura__is_active=True)
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
@apertura_activa
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
        admin = JuntaDirectiva.objects.filter(socio=Socio.objects.get(id=usuario.id)).filter(apertura__is_active=True)
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
@apertura_activa
def del_banner(request,id):
    datos = get_object_or_404(Banner, pk=id)
    datos.delete()
    return HttpResponseRedirect('/administracion/banner')

@backend_login
@apertura_activa
def galeria_fotos(request):
    usuario = Socio.objects.get(username=request.user.username)
    imagenes = Fotos.objects.all().order_by('-id')
    ingresos = Ingreso.objects.filter(socio=usuario)
    temporada = Apertura.objects.get(is_active=True)
    totalI = 0
    try:
        admin = JuntaDirectiva.objects.filter(socio=Socio.objects.get(id=usuario.id)).filter(apertura__is_active=True)
    except:
        admin = False
    for i in ingresos:
        totalI = i.monto+totalI
    el_saldo = temporada.monto_apertura-totalI
    if request.method == 'POST':
        formulario = FormFotos(request.POST,request.FILES)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/administracion/galeria_fotos')
    else:
        formulario = FormFotos()
    cntxt = {
        'imagenes':imagenes, 'formulario':formulario, 'usuario': usuario, 'el_saldo': el_saldo, 'admin': admin,
        }
    return render(request,'backend/galeria_fotos.html',cntxt)

@backend_login
@apertura_activa
def edit_fotos(request,id):
    usuario = Socio.objects.get(username=request.user.username)
    imagenes = Fotos.objects.all().order_by('-id')
    imagen = Fotos.objects.get(id=id)
    ingresos = Ingreso.objects.filter(socio=usuario)
    temporada = Apertura.objects.get(is_active=True)
    totalI = 0
    for i in ingresos:
        totalI = i.monto+totalI
    el_saldo = temporada.monto_apertura-totalI
    try:
        admin = JuntaDirectiva.objects.filter(socio=Socio.objects.get(id=usuario.id)).filter(apertura__is_active=True)
    except:
        admin = False
    if request.method == 'POST':
        formulario = FormFotos(request.POST,request.FILES,instance=imagen)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/administracion/galeria_fotos')
    else:
        formulario = FormFotos(instance=imagen)
    cntxt = {
    'usuario':usuario,
    'imagenes':imagenes,
    'formulario':formulario,
    'el_saldo': el_saldo,
    'admin': admin,
    'imagen': imagen,
    }
    return render (request,'backend/edit_galeria_fotos.html',cntxt)

@backend_login
@apertura_activa
def borrar_fotos(request,id):
    datos = get_object_or_404(Fotos, pk=id)
    datos.delete()
    return HttpResponseRedirect('/administracion/galeria_fotos')

@apertura_activa
def activar_socio(request):
    usuario = Socio.objects.get(username=request.user.username)
    ingresos = Ingreso.objects.filter(socio=usuario)
    temporada = Apertura.objects.get(is_active=True)
    totalI = 0
    for i in ingresos:
        totalI = i.monto+totalI
    el_saldo = temporada.monto_apertura-totalI
    try:
        admin = JuntaDirectiva.objects.filter(socio=Socio.objects.get(id=usuario.id)).filter(apertura__is_active=True)
    except:
        admin = False
    socios = Socio.objects.all()
    cntxt = {
        'socios':socios,'el_saldo': el_saldo, 'admin': admin, 'usuario': usuario,
    }
    return render (request,'backend/activar_socio.html',cntxt)


@backend_login
@apertura_activa
def admin_responsabilidad_social(request):
    responsabilidad_sociales = ResponsabilidadSocial.objects.all()
    usuario = Socio.objects.get(username=request.user.username)
    ingresos = Ingreso.objects.filter(socio=usuario)
    temporada = Apertura.objects.get(is_active=True)
    totalI = 0
    for i in ingresos:
        totalI = i.monto+totalI
    el_saldo = temporada.monto_apertura-totalI
    try:
        admin = JuntaDirectiva.objects.filter(socio=Socio.objects.get(id=usuario.id)).filter(apertura__is_active=True)
    except:
        admin = False
    if request.method == 'POST':
        formulario = FormResponsabilidadSocial(request.POST,request.FILES)
        if formulario.is_valid():
            print "se guardo la responsabilidad social"
            formulario.save()
            return HttpResponseRedirect('/administracion/admin_responsabilidad_social')
    else:
        formulario = FormResponsabilidadSocial()
        print formulario
    cntxt = {
        'usuario':usuario, 'el_saldo': el_saldo, 'admin': admin, 'responsabilidad_sociales': responsabilidad_sociales, 'formulario': formulario,
        }
    return render(request,'backend/responsabilidad_social.html',cntxt)

@backend_login
@apertura_activa
def edit_responsabilidad_social(request,id):
    responsabilidad_sociales = ResponsabilidadSocial.objects.all()
    responsabilidad_social = ResponsabilidadSocial.objects.get(id=id)
    usuario = Socio.objects.get(username=request.user.username)
    ingresos = Ingreso.objects.filter(socio=usuario)
    temporada = Apertura.objects.get(is_active=True)
    totalI = 0
    for i in ingresos:
        totalI = i.monto+totalI
    el_saldo = temporada.monto_apertura-totalI
    try:
        admin = JuntaDirectiva.objects.filter(socio=Socio.objects.get(id=usuario.id)).filter(apertura__is_active=True)
    except:
        admin = False
    if request.method == 'POST':
        formulario = FormResponsabilidadSocial(request.POST,request.FILES,instance=responsabilidad_social)
        if formulario.is_valid():
            print "se guardo la responsabilidad_social"
            formulario.save()
            return HttpResponseRedirect('/administracion/admin_responsabilidad_social')
    else:
        formulario = FormResponsabilidadSocial(instance=responsabilidad_social)
        print formulario
    cntxt = {
        'usuario':usuario, 'el_saldo': el_saldo, 'admin': admin, 'responsabilidad_sociales': responsabilidad_sociales, 'formulario': formulario,
        }
    return render(request,'backend/responsabilidad_social.html',cntxt)

@backend_login
@apertura_activa
def del_responsabilidad_social(request,id):
    datos = get_object_or_404(ResponsabilidadSocial, pk=id)
    datos.delete()
    return HttpResponseRedirect('/administracion/admin_responsabilidad_social')



@backend_login
@apertura_activa
def portadas(request):
    usuario = Socio.objects.get(username=request.user.username)
    imagenes = Portadas.objects.all().order_by('-id')
    ingresos = Ingreso.objects.filter(socio=usuario)
    temporada = Apertura.objects.get(is_active=True)
    totalI = 0
    try:
        admin = JuntaDirectiva.objects.filter(socio=Socio.objects.get(id=usuario.id)).filter(apertura__is_active=True)
    except:
        admin = False
    for i in ingresos:
        totalI = i.monto+totalI
    el_saldo = temporada.monto_apertura-totalI
    if request.method == 'POST':
        formulario = FormPortadas(request.POST,request.FILES)
        print formulario
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/administracion/portadas')
    else:
        formulario = FormPortadas()
    cntxt = {
        'imagenes':imagenes, 'formulario':formulario, 'usuario': usuario, 'el_saldo': el_saldo, 'admin': admin,
        }
    return render(request,'backend/portadas.html',cntxt)

@backend_login
@apertura_activa
def edit_portadas(request,id):
    usuario = Socio.objects.get(username=request.user.username)
    imagenes = Portadas.objects.all().order_by('-id')
    portada = Portadas.objects.get(id=id)
    ingresos = Ingreso.objects.filter(socio=usuario)
    temporada = Apertura.objects.get(is_active=True)
    totalI = 0
    for i in ingresos:
        totalI = i.monto+totalI
    el_saldo = temporada.monto_apertura-totalI
    try:
        admin = JuntaDirectiva.objects.filter(socio=Socio.objects.get(id=usuario.id)).filter(apertura__is_active=True)
    except:
        admin = False
    if request.method == 'POST':
        formulario = FormPortadas(request.POST,request.FILES,instance=portada)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/administracion/portadas')
    else:
        formulario = FormPortadas(instance=portada)
    cntxt = {
    'usuario':usuario,
    'imagenes':imagenes,
    'formulario':formulario,
    'el_saldo': el_saldo,
    'admin': admin,
    }
    return render (request,'backend/portadas.html',cntxt)

@backend_login
@apertura_activa
def del_portadas(request,id):
    datos = get_object_or_404(Portadas, pk=id)
    datos.delete()
    return HttpResponseRedirect('/administracion/portadas')



@login_required(login_url="/")
@apertura_activa
def video_portada(request):
    video_portada = VideoPortada.objects.get(id=1)
    usuario = Socio.objects.get(username=request.user.username)
    print "video_portada.nombre"
    print video_portada.nombre
    print "video_portada.nombre"
    try:
        admin = JuntaDirectiva.objects.filter(socio=Socio.objects.get(id=usuario.id)).filter(apertura__is_active=True)
    except:
        admin = False
    ingresos = Ingreso.objects.filter(socio=usuario)
    temporada = Apertura.objects.get(is_active=True)
    totalI = 0
    for i in ingresos:
        totalI = i.monto+totalI
    el_saldo = temporada.monto_apertura-totalI
    if request.method == 'POST':
        formulario = FormVideoPortada(request.POST,request.FILES,instance=video_portada)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect(reverse('video_portada'))
        else:
            print formulario
    else:
        formulario = FormVideoPortada(instance=usuario)
    cntxt = {
    'usuario':usuario,'formulario':formulario, 'el_saldo': el_saldo, 'admin': admin,'video_portada':video_portada,
    }
    return render (request,'backend/video_portada.html',cntxt)