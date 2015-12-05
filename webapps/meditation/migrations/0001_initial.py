# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=42)),
                ('datetime', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(default=b'meditation/user/no-album-image.jpg', upload_to=b'meditation/album/', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('latitude', models.CharField(default=b'0', max_length=200, blank=True)),
                ('longitude', models.CharField(default=b'0', max_length=200, blank=True)),
                ('datetime', models.DateTimeField(auto_now=True)),
                ('content', models.TextField(max_length=200)),
                ('album', models.ForeignKey(related_name='album_comments', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='meditation.Album', null=True)),
                ('user', models.ForeignKey(related_name='user_comments', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=42)),
                ('latitude', models.CharField(default=b'0', max_length=200, blank=True)),
                ('longitude', models.CharField(default=b'0', max_length=200, blank=True)),
                ('url', models.URLField(default=b'', blank=True)),
                ('datetime', models.DateTimeField(auto_now=True)),
                ('content', models.FileField(null=True, upload_to=b'meditation/music/', blank=True)),
                ('image', models.ImageField(default=b'meditation/user/no-music-image.jpg', upload_to=b'meditation/music/', blank=True)),
                ('user', models.ForeignKey(related_name='user_musics', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=42, blank=True)),
                ('content', models.CharField(default=b'', max_length=2000, blank=True)),
                ('image', models.ImageField(default=b'meditation/user/no-news-image.jpg', upload_to=b'meditation/news/', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(default=b'', max_length=20, blank=True)),
                ('last_name', models.CharField(default=b'', max_length=20, blank=True)),
                ('dob', models.DateField(null=True, blank=True)),
                ('phone', models.CharField(default=b'', max_length=20, blank=True)),
                ('address', models.CharField(default=b'', max_length=100, blank=True)),
                ('bio', models.TextField(default=b'', max_length=1000, blank=True)),
                ('image', models.ImageField(default=b'meditation/user/no-user-image.jpg', upload_to=b'meditation/user/', blank=True)),
                ('favorites', models.ManyToManyField(related_name='user_favorite_albums', to='meditation.Album', blank=True)),
                ('user', models.OneToOneField(related_name='user_profile', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=42, blank=True)),
                ('content', models.CharField(default=b'', max_length=3000, blank=True)),
                ('user', models.ForeignKey(related_name='user_recommendation', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sound',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=42)),
                ('latitude', models.CharField(default=b'0', max_length=200, blank=True)),
                ('longitude', models.CharField(default=b'0', max_length=200, blank=True)),
                ('url', models.URLField(default=b'', blank=True)),
                ('datetime', models.DateTimeField(auto_now=True)),
                ('content', models.FileField(null=True, upload_to=b'meditation/sound/', blank=True)),
                ('image', models.ImageField(default=b'meditation/user/no-sound-image.jpg', upload_to=b'meditation/sound/', blank=True)),
                ('user', models.ForeignKey(related_name='user_sounds', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='album',
            name='musics',
            field=models.ManyToManyField(related_name='music_albums', to='meditation.Music', blank=True),
        ),
        migrations.AddField(
            model_name='album',
            name='sound',
            field=models.ForeignKey(related_name='sound_albums', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='meditation.Sound', null=True),
        ),
        migrations.AddField(
            model_name='album',
            name='user',
            field=models.ForeignKey(related_name='user_albums', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
