from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from administracion.forms import FormSocio
from backend.models import Apertura

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