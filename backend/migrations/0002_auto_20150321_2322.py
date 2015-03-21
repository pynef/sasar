# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='apertura',
            name='fin',
            field=models.DateField(default=datetime.date(2015, 3, 21)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='apertura',
            name='incio',
            field=models.DateField(default=datetime.date(2015, 3, 21)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='apertura',
            name='temporada',
            field=models.CharField(default=b'temporada 2014', max_length=128),
            preserve_default=True,
        ),
    ]
