# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0019_auto_20150411_0745'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fotos',
            name='nombre',
        ),
        migrations.AddField(
            model_name='fotos',
            name='foto',
            field=models.ImageField(null=True, upload_to=b'Fotos/', blank=True),
            preserve_default=True,
        ),
    ]
