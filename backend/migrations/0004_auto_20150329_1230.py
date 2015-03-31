# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_auto_20150322_0122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socio',
            name='picture',
            field=models.ImageField(default=b'default/avatar.png', null=True, upload_to=b'Socios/', blank=True),
            preserve_default=True,
        ),
    ]
