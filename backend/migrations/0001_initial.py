# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Apertura',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('saldo_anterior', models.DecimalField(max_digits=6, decimal_places=2)),
                ('monto_apertura', models.DecimalField(max_digits=6, decimal_places=2)),
                ('temporada', models.IntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=64)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Egreso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('recibo', models.CharField(max_length=64)),
                ('concepto', models.CharField(max_length=64)),
                ('monto', models.DecimalField(max_digits=6, decimal_places=2)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('apertura', models.ForeignKey(to='backend.Apertura')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ingreso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('recibo', models.CharField(max_length=64)),
                ('monto', models.DecimalField(max_digits=6, decimal_places=2)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('apertura', models.ForeignKey(to='backend.Apertura')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='JuntaDirectiva',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('apertura', models.ForeignKey(to='backend.Apertura')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Socio',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('resumen', models.TextField(null=True, blank=True)),
                ('direccion', models.CharField(max_length=128, null=True, blank=True)),
                ('dni', models.CharField(unique=True, max_length=8)),
                ('fecha_nacimiento', models.DateField(null=True, blank=True)),
                ('ocupacion', models.CharField(max_length=64, null=True, blank=True)),
                ('residencia', models.CharField(max_length=128, null=True, blank=True)),
                ('picture', models.ImageField(default=b'default/company.png', null=True, upload_to=b'Personal/', blank=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('categoria', models.ForeignKey(blank=True, to='backend.Categoria', null=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
        ),
        migrations.AddField(
            model_name='juntadirectiva',
            name='socio',
            field=models.ForeignKey(to='backend.Socio'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ingreso',
            name='socio',
            field=models.ForeignKey(to='backend.Socio'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='egreso',
            name='socio',
            field=models.ForeignKey(to='backend.Socio'),
            preserve_default=True,
        ),
    ]
