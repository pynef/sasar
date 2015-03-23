from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from administracion.forms import FormSocio, FormIngreso, FormEgreso, formSocio
from backend.models import Apertura, Ingreso, Socio, Egreso, JuntaDirectiva

def home(request):
	return render(request,'frontend/index.html')

def temporada(req):
    temporada = Apertura.objects.all().order_by('-fin')[0]
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
      'form': form
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
    apertura = Apertura.objects.get(is_active=True)
    ultimos_pagos = Ingreso.objects.all().order_by('-create_at')[:4]
    if req.method == 'POST':
        formulario = FormIngreso(req.POST)
        if formulario.is_valid():
            ingreso=formulario.save()
        else:
            print formulario
    else:
        formulario = FormIngreso()
    ctx = {
        'formulario' : formulario, 'apertura' : apertura, 'ultimos_pagos': ultimos_pagos,
    }
    return render(req, 'backend/ingresos.html',ctx)

def egresos(req):
    apertura = Apertura.objects.get(is_active=True)
    usuario = Socio.objects.get(username=req.user.username)
    ultimos_pagos = Egreso.objects.all().order_by('-create_at')[:5]
    if req.method == 'POST':
        formulario = FormEgreso(req.POST)
        if formulario.is_valid():
            ingreso=formulario.save()
        else:
            print formulario
    else:
        formulario = FormEgreso()
    ctx = {
        'formulario' : formulario, 'apertura' : apertura, 'ultimos_pagos': ultimos_pagos, 'usuario': usuario,
    }
    return render(req, 'backend/egresos.html',ctx)

def perfil(request):
    usuario = Socio.objects.get(username=request.user.username)
    if request.method == 'POST':
        formulario = formSocio(request.POST,request.FILES,instance=usuario)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/panel')
    else:
        formulario = formSocio(instance=usuario)
    cntxt = {
    'usuario':usuario,'formulario':formulario,
    }
    return render (request,'backend/profile.html',cntxt)

def junta_directiva(request):
    junta_directiva = JuntaDirectiva.objects.filter(apertura__is_active=True)
    print junta_directiva
    cntxt = {
        'junta_directiva':junta_directiva,
        }
    return render(request,'backend/junta_directiva.html',cntxt)