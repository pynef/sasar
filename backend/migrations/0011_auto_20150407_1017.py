# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0010_noticias_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=64)),
                ('descripcion', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='juntadirectiva',
            name='cargo',
            field=models.ForeignKey(blank=True, to='backend.Cargo', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='socio',
            name='orden_parada',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
