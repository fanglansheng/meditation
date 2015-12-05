from django.shortcuts import render
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from meditation.forms import *


@transaction.atomic
@csrf_exempt
def create_sound_plugin(request):
    if not request.user.is_authenticated():
        return render(request, 'meditation/plugin-panel.html',
                      {'text': 'Error: Please login to your account and try again.'})
    if request.method == 'GET':
        return render(request, 'meditation/plugin-panel.html', {'text': 'Error: Request is GET.'})
    if 'https://www.youtube.com/watch?v=' not in request.POST['url']:
        return render(request, 'meditation/plugin-panel.html',
                      {'text': 'Error: This page seems no sound. Launch a youtube video and try again.'})
    try:
        new_sound = Sound(user=request.user)
    except:
        return render(request, 'meditation/plugin-panel.html',
                      {'text': 'Error: An error occurred, no profile found, please login and try again.'})
    form = CreateSoundForm(request.POST, instance=new_sound)
    if not form.is_valid():
        return render(request, 'meditation/plugin-panel.html', {'text': 'Error: Input not valid, please try again.'})
    form.save()
    return render(request, 'meditation/plugin-panel.html',
                  {'text': 'Success adding this sound. Refresh to see changes.'})


@transaction.atomic
@csrf_exempt
def create_music_plugin(request):
    if not request.user.is_authenticated():
        return render(request, 'meditation/plugin-panel.html',
                      {'text': 'Error: Please login to your account and try again.'})
    if request.method == 'GET':
        return render(request, 'meditation/plugin-panel.html', {'text': 'Error: Request is GET.'})
    if 'https://www.youtube.com/watch?v=' not in request.POST['url']:
        return render(request, 'meditation/plugin-panel.html',
                      {'text': 'Error: This page seems no music. Launch a youtube video and try again.'})
    try:
        new_music = Music(user=request.user)
    except:
        return render(request, 'meditation/plugin-panel.html',
                      {'text': 'Error: An error occurred, no profile found, please login and try again.'})
    form = CreateMusicForm(request.POST, instance=new_music)
    if not form.is_valid():
        return render(request, 'meditation/plugin-panel.html', {'text': 'Error: Input not valid, please try again.'})
    form.save()
    return render(request, 'meditation/plugin-panel.html',
                  {'text': 'Success adding this music. Refresh to see changes.'})
