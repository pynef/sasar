# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0015_multimediafotos_socio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='multimediafotos',
            name='socio',
            field=models.ForeignKey(to='backend.Socio'),
            preserve_default=True,
        ),
    ]
