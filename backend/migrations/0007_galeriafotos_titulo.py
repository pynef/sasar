# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_auto_20150329_1531'),
    ]

    operations = [
        migrations.AddField(
            model_name='galeriafotos',
            name='titulo',
            field=models.CharField(max_length=128, null=True, blank=True),
            preserve_default=True,
        ),
    ]
