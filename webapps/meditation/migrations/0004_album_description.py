# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meditation', '0003_auto_20151203_1315'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='description',
            field=models.TextField(default=b'', max_length=200, blank=True),
        ),
    ]
