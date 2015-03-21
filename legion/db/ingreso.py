#enconding:utf-8
from django.contrib.auth.models import User,Group
from backend.models import Categoria,Socio,Apertura,Ingreso,Egreso,JuntaDirectiva


b=Group.objects.create(
	name = 'backend'
	)
a=Group.objects.create(
	name = 'administracion'
	)
f=Group.objects.create(
	name = 'frontend'
	)


backend = Socio.objects.create(dni=11111111,username = "backend")
backend.groups.add(b)
backend.set_password("backend")
backend.save()

administracion=Socio.objects.create(dni=22222222,username = "administracion")
administracion.groups.add(a)
administracion.set_password("administracion")
administracion.save()

frontend=Socio.objects.create(dni=33333333,username = "frontend")
frontend.groups.add(f)
frontend.set_password("frontend")
frontend.save()