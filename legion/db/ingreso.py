#enconding:utf-8
from django.contrib.auth.models import User,Group
from backend.models import Categoria,Socio,Apertura,Ingreso,Egreso,JuntaDirectiva, Cargo


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

administracion=Socio.objects.create(dni=22222222,username = "administrador")
administracion.groups.add(b)
administracion.set_password("administrador")
administracion.save()

frontend=Socio.objects.create(dni=33333333,username = "usuario")
frontend.groups.add(f)
frontend.set_password("usuario")
frontend.save()


p=Cargo.objects.create(nombre = "Presidencia")
sp=Cargo.objects.create(nombre = "Sub-presidente")
t=Cargo.objects.create(nombre = "Tesorero")
s=Cargo.objects.create(nombre = "Secretario")
v=Cargo.objects.create(nombre = "Vocal")


a=Categoria.objects.create(nombre = "Activo")
i=Categoria.objects.create(nombre = "Inactivo")
r=Categoria.objects.create(nombre = "Retirado")
j=Categoria.objects.create(nombre = "Jubilado")
n=Categoria.objects.create(nombre = "Neutro")

apertura=Apertura.objects.create(saldo_anterior=0,monto_apertura=350,temporada="temporada 2014-2015",inicio="2014-08-01",fin="2014-08-01")
junta=JuntaDirectiva.objects.create(socio=backend,apertura=apertura,cargo=p)