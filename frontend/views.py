# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.models import User,Group
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from legion.decoratos import administrador_login,backend_login,frontend_login



def home(request):
    return render(request,'frontend/index.html')

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
        return HttpResponseRedirect('/home/ ')