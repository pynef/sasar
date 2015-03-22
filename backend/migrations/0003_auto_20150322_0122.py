# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_auto_20150321_2322'),
    ]

    operations = [
        migrations.RenameField(
            model_name='apertura',
            old_name='incio',
            new_name='inicio',
        ),
        migrations.AlterField(
            model_name='apertura',
            name='monto_apertura',
            field=models.DecimalField(default=0, max_digits=6, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='apertura',
            name='saldo_anterior',
            field=models.DecimalField(default=0, max_digits=6, decimal_places=2),
            preserve_default=True,
        ),
    ]
