# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0014_remove_multimediafotos_socio'),
    ]

    operations = [
        migrations.AddField(
            model_name='multimediafotos',
            name='socio',
            field=models.ForeignKey(blank=True, to='backend.Socio', null=True),
            preserve_default=True,
        ),
    ]
