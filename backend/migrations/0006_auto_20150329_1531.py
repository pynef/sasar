# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_auto_20150329_1519'),
    ]

    operations = [
        migrations.RenameField(
            model_name='galeriafotos',
            old_name='nomre',
            new_name='nombre',
        ),
    ]
