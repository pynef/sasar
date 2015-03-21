# -*- encoding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm, TextInput, Select, Textarea, FileInput, PasswordInput
from backend.models import Socio


class formSocio(ModelForm):
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