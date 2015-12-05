from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from meditation.forms import *
import json


def get_all_albums(request):
    all_albums = [a.to_json() for a in Album.objects.all()]
    data = json.dumps(all_albums)
    return HttpResponse(data, content_type='application/json')


def get_all_sounds(request):
    all_sounds = [s.to_json() for s in Sound.objects.all()]
    data = json.dumps(all_sounds)

    return HttpResponse(data, content_type='application/json')


def get_all_musics(request):
    all_music = [m.to_json() for m in Music.objects.all()]
    data = json.dumps(all_music)
    return HttpResponse(data, content_type='application/json')


@login_required
def get_others_albums(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_albums = [a.to_json() for a in user.user_albums.all()]
    data = json.dumps(user_albums)
    return HttpResponse(data, content_type='application/json')


@login_required
def get_others_sounds(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_sounds = [s.to_json() for s in Sound.objects.filter(user=user)]
    data = json.dumps(user_sounds)
    return HttpResponse(data, content_type='application/json')


@login_required
def get_others_favorite_albums(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_favorite_albums = [a.to_json() for a in user.user_profile.favorites.all()]
    data = json.dumps(user_favorite_albums)
    return HttpResponse(data, content_type='application/json')


@login_required
def get_user_albums(request):
    user = request.user
    user_albums = [a.to_json() for a in user.user_albums.all()]
    data = json.dumps(user_albums)
    return HttpResponse(data, content_type='application/json')


@login_required
def get_user_sounds(request):
    user = request.user
    user_sounds = [s.to_json() for s in Sound.objects.filter(user=user)]
    data = json.dumps(user_sounds)
    return HttpResponse(data, content_type='application/json')


@login_required
def get_user_musics(request):
    user = request.user
    user_musics = [m.to_json() for m in Music.objects.filter(user=user)]
    data = json.dumps(user_musics)
    return HttpResponse(data, content_type='application/json')


@login_required
def get_user_favorite_albums(request):
    user = request.user
    user_favorite_albums = [a.to_json() for a in user.user_profile.favorites.all()]
    data = json.dumps(user_favorite_albums)
    return HttpResponse(data, content_type='application/json')


@login_required
def get_sound_id(request, sound_id):
    sound = get_object_or_404(Sound, id=sound_id)
    return HttpResponse(json.dumps(sound), content_type='application/json')


# get albums in selected sound
def get_albums(requset, sound_id):
    sound = get_object_or_404(Sound, id=sound_id)
    albums = [a.to_json() for a in Album.objects.filter(sound=sound)]
    data = json.dumps(albums)
    return HttpResponse(data, content_type='application/json')


@login_required
def get_user(request):
    dic = {}
    try:
        dic['type'] = 'success'
        dic['user'] = user_to_json(request.user)
    except:
        dic['type'] = 'error'
        dic['errors'] = 'error getting user.'
    data = json.dumps(dic)
    return HttpResponse(data, content_type='application/json')
