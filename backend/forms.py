# -*- encoding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm, TextInput, Select, Textarea, FileInput, PasswordInput
from backend.models import Apertura, Ingreso, Egreso, Socio, GaleriaFotos, User, Noticias, Banner, Fotos, JuntaDirectiva


class FormSocio(ModelForm):
    class Meta:
        model = Apertura
        exclude =  [
                    'is_active',
                    'saldo_anterior'
                    ]
        widgets={
            'username': TextInput(attrs={'class': 'form-control'}),
            'monto_apertura': TextInput(attrs={'class': 'form-control', 'type':'number', 'min-length':'2' }),
            'temporada': TextInput(attrs={'class': 'form-control'}),
            'inicio': TextInput(attrs={'class': 'form-control data-input', 
                                    'data-inputmask': "'alias': 'dd/mm/yyyy'",
                                    'data-mask':''}),
            'fin': TextInput(attrs={'class': 'form-control data-input', 
                                    'data-inputmask': "'alias': 'dd/mm/yyyy'",
                                    'data-mask':''}),
        }

class FormIngreso(ModelForm):
    class Meta:
        model = Ingreso


class FormEgreso(ModelForm):
    class Meta:
        model = Egreso


class formSocios(ModelForm):
    class Meta:
        model = Socio
        exclude =  [
                    'last_login',
                    'is_superuser',
                    'is_staff',
                    'date_joined',
                    'user_permissions',
                    'password',
                    'groups',
                    'is_active',
                    ]
        widgets={
            'username': TextInput(attrs={'class': 'form-control'}),
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'email': TextInput(attrs={'class': 'form-control'}),
            'resumen': TextInput(attrs={'class': 'form-control'}),
            'direccion': TextInput(attrs={'class': 'form-control'}),
            'dni': TextInput(attrs={'class': 'form-control'}),
            'ocupacion': TextInput(attrs={'class': 'form-control'}),
            'residencia': TextInput(attrs={'class': 'form-control'}),
            'categoria': Select(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'orden_parada': TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'avatar': FileInput(attrs={'class': 'form-control'}),
        }


class FormGaleriaFotos(ModelForm):
    class Meta:
        model = GaleriaFotos


class FormFotos(ModelForm):
    class Meta:
        model = Fotos


class FormGaleriaFotosEdit(ModelForm):
    class Meta:
        model = GaleriaFotos
        exclude =  [
                    'socio',
                    ]
        widgets={
            'titulo': TextInput(attrs={'class': 'form-control'}),
            'descripcion': Textarea(attrs={'cols': 23, 'rows': 2,'class':'form-control'}),
        }


class FormSocioVideo(ModelForm):
    class Meta:
        model = Socio
        fields  =  [
                    'video',
                    ]

class userForm(ModelForm):
    class Meta():
        model = Socio
        exclude =  ['active',
                    'last_login',
                    'is_superuser',
                    'is_staff',
                    'date_joined',
                    'auth_permission',
                    'user_permissions',
                    'groups']
        widgets = {
            'password': forms.PasswordInput(),
            'dni': TextInput(attrs={'class': 'form-control'}),
            'username': TextInput(attrs={'class': 'form-control'}),
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'email': TextInput(attrs={'class': 'form-control'}),
            'orden_parada': TextInput(attrs={'class': 'form-control data-input', 
                                    'data-inputmask': "'alias': 'dd/mm/yyyy'",
                                    'data-mask':''}),
        }

class FormNoticias(ModelForm):
    class Meta:
        model = Noticias
        fields  =  [
                    'picture','titulo','descripcion','user',
                    ]
        widgets = {
            'picture': FileInput(attrs={'class': 'form-control form-space'}),
            'titulo': TextInput(attrs={'class': 'form-control form-space'}),
            'descripcion': Textarea(attrs={'cols': 23, 'rows': 2,'class':'form-control form-space'}),
        }


class FormBanner(ModelForm):
    class Meta:
        model = Banner
        fields  =  [
                    'picture','titulo','descripcion','user',
                    ]
        widgets = {
            'picture': FileInput(attrs={'class': 'form-control form-space'}),
            'titulo': TextInput(attrs={'class': 'form-control form-space'}),
            'descripcion': Textarea(attrs={'cols': 23, 'rows': 2,'class':'form-control form-space'}),
        }
        

class FormJuntaDirectiva(ModelForm):
    class Meta:
        model = JuntaDirectiva