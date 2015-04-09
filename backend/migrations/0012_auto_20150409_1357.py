# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0011_auto_20150407_1017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socio',
            name='categoria',
            field=models.ForeignKey(default=b'Activo', blank=True, to='backend.Categoria', null=True),
            preserve_default=True,
        ),
    ]
