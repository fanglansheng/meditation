from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
from meditation.forms import *
from mimetypes import guess_type


def get_user_image(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=user)

    if not profile.image:
        raise Http404
    content_type = guess_type(profile.image.name)
    return HttpResponse(profile.image, content_type=content_type)


def get_album_image(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    if not album.image:
        raise Http404
    content_type = guess_type(album.image.name)
    return HttpResponse(album.image, content_type=content_type)


def get_sound_image(request, sound_id):
    sound = get_object_or_404(Sound, id=sound_id)
    if not sound.image:
        raise Http404
    content_type = guess_type(sound.image.name)
    return HttpResponse(sound.image, content_type=content_type)


def get_music_image(request, music_id):
    music = get_object_or_404(Music, id=music_id)
    if not music.image:
        raise Http404
    content_type = guess_type(music.image.name)
    return HttpResponse(music.image, content_type=content_type)


def get_sound_content(request, sound_id):
    sound = get_object_or_404(Sound, id=sound_id)
    if not sound.content:
        raise Http404
    content_type = guess_type(sound.content.name)
    return HttpResponse(sound.content, content_type=content_type)


def get_music_content(request, music_id):
    music = get_object_or_404(Music, id=music_id)
    if not music.content:
        raise Http404
    content_type = guess_type(music.content.name)
    return HttpResponse(music.content, content_type=content_type)
