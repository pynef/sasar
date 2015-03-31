# -*- encoding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm, TextInput, Select, Textarea, FileInput, PasswordInput
from backend.models import Apertura, Ingreso, Egreso, Socio, GaleriaFotos


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
                    ]
        widgets={
            'username': TextInput(attrs={'class': 'form-control'}),
        }


class FormGaleriaFotos(ModelForm):
    class Meta:
        model = GaleriaFotos


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