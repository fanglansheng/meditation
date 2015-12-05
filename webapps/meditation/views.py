from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from meditation.forms import *


# home that can be accessed by all people without logging in
@login_required
def home(request):
    context = {}
    context['create_sound_form'] = CreateSoundForm()
    context['create_music_form'] = CreateMusicForm()
    context['create_album_form'] = CreateAlbumForm()
    context['profile_form'] = ProfileForm()
    return render(request, 'meditation/home.html', context)


# home that can be accessed by logged in users, eg. logout button
def home_login(request):
    context = {}
    context['login_form'] = MyAuthenticationForm()
    context['register_form'] = RegistrationForm()
    context['reset_password_form'] = MyPasswordResetForm()
    return render(request, 'meditation/home.html', context)


# user sound and music can have a delete button, which is to delete from database
# all sound and music are used to search
@login_required
def album_management(request):
    context = {}
    context['create_sound_form'] = CreateSoundForm()
    context['create_music_form'] = CreateMusicForm()
    context['create_album_form'] = CreateAlbumForm()
    return render(request, 'meditation/album-management.html', context)


# go to user profile
@login_required
def user_profile(request, user_id):
    context = {}
    context['user'] = get_object_or_404(User, id=user_id)
    context['profile_form'] = ProfileForm()
    context['change_password_form'] = MyPasswordChangeForm(user=request.user)
    context['create_sound_form'] = CreateSoundForm()
    context['create_music_form'] = CreateMusicForm()
    context['create_album_form'] = CreateAlbumForm()
    return render(request, 'meditation/user-profile.html', context)


def getPartialHtml(request, urlPath):
    return render(request, 'meditation/' + urlPath)
