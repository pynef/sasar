# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0018_delete_multimediafotos'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fotos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.ImageField(null=True, upload_to=b'MultimediaFotos/', blank=True)),
                ('titulo', models.CharField(max_length=128, null=True, blank=True)),
                ('descripcion', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='noticias',
            name='is_active',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
