# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0017_remove_multimediafotos_socio'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MultimediaFotos',
        ),
    ]
