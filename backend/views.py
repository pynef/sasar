from django.shortcuts import render
from django.contrib.auth.models import User,Group
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from legion.decoratos import administrador_login,backend_login,frontend_login
from backend.forms import formSocio
from backend.models import Socio,JuntaDirectiva

@backend_login
def index(request):
	usuario = Socio.objects.get(username=request.user.username)
	print usuario
	cntxt = {
        'usuario':usuario,
        }
        return render(request,'backend/index.html',cntxt)

@backend_login
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

@backend_login
def junta_directiva(request):
    junta_directiva = JuntaDirectiva.objects.filter(apertura__is_active=True)
    print junta_directiva
    cntxt = {
        'junta_directiva':junta_directiva,
        }
    return render(request,'backend/junta_directiva.html',cntxt)