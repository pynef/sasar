# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0012_auto_20150409_1357'),
    ]

    operations = [
        migrations.CreateModel(
            name='MultimediaFotos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.ImageField(null=True, upload_to=b'MultimediaFotos/', blank=True)),
                ('titulo', models.CharField(max_length=128, null=True, blank=True)),
                ('descripcion', models.TextField(null=True, blank=True)),
                ('socio', models.ForeignKey(blank=True, to='backend.Socio', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='socio',
            name='categoria',
            field=models.ForeignKey(blank=True, to='backend.Categoria', null=True),
            preserve_default=True,
        ),
    ]
