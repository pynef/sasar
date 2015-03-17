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


class Socio(models.Model):
    '''
      Modelos de la clase Socio
      Se relaciona 1:1 con el User
    '''
    nombres = models.CharField(max_length=64)
    apellidos = models.CharField(max_length=64)
    resumen = models.TextField()
    direccion = models.CharField(max_length=128)
    dni = models.CharField(max_length=8, unique=True)
    fecha_nacimiento = models.DateField()
    ocupacion = models.CharField(max_length=64)
    residencia = models.CharField(max_length=128)
    email = models.EmailField(max_length=64)
    is_active = models.BooleanField()
    picture = models.ImageField(upload_to="uploads/",
                                default='default/company.png')
    categoria = models.ForeignKey(Categoria)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{0}'.format(self.nombres)


class Apertura(models.Model):
    '''
      Cuenta contab
      un socio puede tener varias cuentas
      una cuenta solo tiene un socio
    '''
    saldo_anterior = models.DecimalField(decimal_places=2, max_digits=6)
    monto_apertura = models.DecimalField(decimal_places=2, max_digits=6)
    temporada = models.IntegerField()
    is_active = models.BooleanField()
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
    apertura = models.ForeignKey(Socio)
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
    apertura = models.ForeignKey(Socio)
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
    apertura = models.ForeignKey(apertura)

    def __str__(self):
        return '{0}'.format(self.socio)
