# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_galeriafotos_titulo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='galeriafotos',
            name='nombre',
            field=models.ImageField(null=True, upload_to=b'GaleriaFotos/', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='socio',
            name='video',
            field=models.FileField(null=True, upload_to=b'VideoSocio', blank=True),
            preserve_default=True,
        ),
    ]
