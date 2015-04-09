# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_auto_20150402_0849'),
    ]

    operations = [
        migrations.AddField(
            model_name='noticias',
            name='is_active',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
