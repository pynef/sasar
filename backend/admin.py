from django.contrib import admin

from backend.models import Categoria
from backend.models import Socio
from backend.models import Apertura
from backend.models import Ingreso
from backend.models import Egreso
from backend.models import JuntaDirectiva
from backend.models import GaleriaFotos

admin.site.register(Categoria)
admin.site.register(Socio)
admin.site.register(Apertura)
admin.site.register(Ingreso)
admin.site.register(Egreso)
admin.site.register(JuntaDirectiva)
admin.site.register(GaleriaFotos)