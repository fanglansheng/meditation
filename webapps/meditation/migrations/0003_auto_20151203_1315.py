# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meditation', '0002_auto_20151122_2115'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='longitude',
        ),
        migrations.RemoveField(
            model_name='music',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='music',
            name='longitude',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='address',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='dob',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='sound',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='sound',
            name='longitude',
        ),
    ]
