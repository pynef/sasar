# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0016_auto_20150411_0735'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='multimediafotos',
            name='socio',
        ),
    ]
