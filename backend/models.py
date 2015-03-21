from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


class Categoria(models.Model):
    '''
      Categoria en la que entra
      el Socio
    '''
    nombre = models.CharField(max_length=64)

    def __str__(self):
        return '{0}'.format(self.nombre)


class Socio(User):
    '''
      Modelos de la clase Socio
      Se relaciona 1:1 con el User
    '''
    resumen = models.TextField(blank=True, null=True)
    direccion = models.CharField(max_length=128,blank=True, null=True)
    dni = models.CharField(max_length=8, unique=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    ocupacion = models.CharField(max_length=64,blank=True, null=True)
    residencia = models.CharField(max_length=128,blank=True, null=True)
    picture = models.ImageField(upload_to="Personal/",
                                default='default/company.png',blank=True, null=True)
    categoria = models.ForeignKey(Categoria,blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{0}'.format(self.dni)


class Apertura(models.Model):
    '''
      Cuenta contab
      un socio puede tener varias cuentas
      una cuenta solo tiene un socio
    '''
    saldo_anterior = models.DecimalField(decimal_places=2, max_digits=6)
    monto_apertura = models.DecimalField(decimal_places=2, max_digits=6)
    temporada = models.CharField(max_length=128, default="temporada 2014")
    incio = models.DateField()
    fin = models.DateField()
    is_active = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{0}'.format(self.temporada)


class Ingreso(models.Model):
    '''
      Informacion de ingreso de dinero de un
      socio a una apertura
    '''
    recibo = models.CharField(max_length=64)
    socio = models.ForeignKey(Socio)
    monto = models.DecimalField(decimal_places=2, max_digits=6)
    apertura = models.ForeignKey(Apertura)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{0}'.format(self.recibo)


class Egreso(models.Model):
    '''
      Informacion de egresos de una determinada
      apertura
    '''
    recibo = models.CharField(max_length=64)
    concepto = models.CharField(max_length=64)
    socio = models.ForeignKey(Socio)
    monto = models.DecimalField(decimal_places=2, max_digits=6)
    apertura = models.ForeignKey(Apertura)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{0}'.format(self.recibo)


class JuntaDirectiva(models.Model):
    '''
      Lista de socios que conforma la junta directiva
       de una determinada apertura
    '''
    socio = models.ForeignKey(Socio)
    apertura = models.ForeignKey(Apertura)

    def __str__(self):
        return '{0}'.format(self.socio)
