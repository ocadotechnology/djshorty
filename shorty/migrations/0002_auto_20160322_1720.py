# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shorty', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shorturl',
            options={'ordering': ('created',)},
        ),
        migrations.AlterField(
            model_name='shorturl',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
    ]
