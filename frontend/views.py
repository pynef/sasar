# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.models import User,Group
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from legion.decoratos import backend_login,frontend_login
from backend.models import Socio, GaleriaFotos, Ingreso, Apertura, Noticias, Banner, Fotos, Portadas, VideoPortada, ResponsabilidadSocial


def inicio(request):
    portadas = Portadas.objects.all()
    noti = Banner.objects.all().order_by('-id')[:1].get()
    print "notficacion"
    print noti
    print "notficacion"
    cntxt={
        'noti':noti,'portadas':portadas,
    }
    return render(request,'frontend/index.html',cntxt)

def home(request):
    noti = Banner.objects.all().order_by('-id')[:1]
    portadas = Portadas.objects.all()
    video_portada = VideoPortada.objects.get(id=1)
    cntxt={
        'noti':noti,
        'portadas':portadas,
        'video_portada':video_portada,
    }
    return render(request,'frontend/index.html',cntxt)

def responsabilidad_social(request):
    portadas = Portadas.objects.all()
    las_noticias = ResponsabilidadSocial.objects.all()
    print portadas
    cntxt={
        'portadas':portadas,'las_noticias':las_noticias,
    }
    return render(request,'frontend/responsabilidad_social.html',cntxt)

def quienes_somos(request):
    portadas = Portadas.objects.all()
    cntxt={
        'portadas':portadas,
    }
    return render(request,'frontend/quienes_somos.html',cntxt)

def reglamentos(request):
    portadas = Portadas.objects.all()
    cntxt={
        'portadas':portadas,
    }
    return render(request,'frontend/reglamentos.html',cntxt)

def estatutos(request):
    portadas = Portadas.objects.all()
    cntxt={
        'portadas':portadas,
    }
    return render(request,'frontend/estatutos.html',cntxt)

def informes(request):
    portadas = Portadas.objects.all()
    cntxt={
        'portadas':portadas,
    }
    return render(request,'frontend/informes.html',cntxt)

def periodismo(request):
    portadas = Portadas.objects.all()
    cntxt={
        'portadas':portadas,
    }
    return render(request,'frontend/periodismo.html',cntxt)

def galeria_multimedia(request):
    portadas = Portadas.objects.all()
    cntxt={
        'portadas':portadas,
    }
    return render(request,'frontend/galeria_multimedia.html',cntxt)

def socios(request):
    portadas = Portadas.objects.all()
    usuarios = Socio.objects.all()
    print usuarios
    cntxt={
        'usuarios':usuarios,'portadas':portadas,
    }
    return render(request,'frontend/socios.html',cntxt)

def las_noticias(request):
    portadas = Portadas.objects.all()
    las_noticias = Noticias.objects.all()
    cntxt={
        'las_noticias':las_noticias,'portadas':portadas,
    }
    return render(request,'frontend/las_noticias.html',cntxt)

def socio(request,dni):
    portadas = Portadas.objects.all()
    socio = Socio.objects.get(dni=dni)
    galeria_imagenes = GaleriaFotos.objects.filter(socio=Socio.objects.get(dni=dni))
    cntxt={
        'socio':socio, 'galeria_imagenes': galeria_imagenes,'portadas':portadas,
    }
    return render(request,'frontend/socio.html',cntxt)

def index(request):
    portadas = Portadas.objects.all()
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

def fotos_socios(request):
    portadas = Portadas.objects.all()
    fotoSocios = Socio.objects.all()
    cntxt={
        'fotoSocios':fotoSocios,'portadas':portadas,
    }
    return render(request,'frontend/fotos_socios.html',cntxt)

def fotos_galeria(request):
    portadas = Portadas.objects.all()
    fotoGaleria = Fotos.objects.all()
    cntxt={
        'fotoGaleria':fotoGaleria,'portadas':portadas,
    }
    print fotoGaleria
    return render(request,'frontend/fotos_galeria.html',cntxt)

def videos_galeria(request):
    portadas = Portadas.objects.all()
    videosSocios = Socio.objects.all()
    cntxt={
        'videosSocios':videosSocios,'portadas':portadas,
    }
    return render(request, 'frontend/videos_galeria.html', cntxt)

def video(request,id):
    portadas = Portadas.objects.all()
    socio = Socio.objects.get(id=id)
    cntxt={
        'socio':socio,'portadas':portadas,
    }
    return render(request,'frontend/video.html',cntxt)
