# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_auto_20150329_1230'),
    ]

    operations = [
        migrations.CreateModel(
            name='GaleriaFotos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nomre', models.ImageField(null=True, upload_to=b'Socios/', blank=True)),
                ('descripcion', models.TextField(null=True, blank=True)),
                ('socio', models.ForeignKey(to='backend.Socio')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='socio',
            name='video',
            field=models.FileField(null=True, upload_to=b'', blank=True),
            preserve_default=True,
        ),
    ]
