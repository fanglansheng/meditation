# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meditation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='image',
            field=models.ImageField(default=b'meditation/album/no-album-image.jpg', upload_to=b'meditation/album/', blank=True),
        ),
        migrations.AlterField(
            model_name='music',
            name='image',
            field=models.ImageField(default=b'meditation/music/no-music-image.jpg', upload_to=b'meditation/music/', blank=True),
        ),
        migrations.AlterField(
            model_name='music',
            name='url',
            field=models.URLField(default=b''),
        ),
        migrations.AlterField(
            model_name='news',
            name='image',
            field=models.ImageField(default=b'meditation/news/no-news-image.jpg', upload_to=b'meditation/news/', blank=True),
        ),
        migrations.AlterField(
            model_name='sound',
            name='image',
            field=models.ImageField(default=b'meditation/sound/no-sound-image.jpg', upload_to=b'meditation/sound/', blank=True),
        ),
    ]
