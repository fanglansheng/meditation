from django.shortcuts import get_object_or_404
from django.db import transaction
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from meditation.forms import *
import json


@login_required
def get_user_profile(request, user_id):
    dic = {}
    try:
        user = get_object_or_404(User, id=user_id)
        new_profile = get_object_or_404(Profile, user=user)
        dic['type'] = 'success'
        dic['profile'] = new_profile.to_json()
    except:
        dic['type'] = 'error'
        dic['errors'] = 'error getting user profile.'
    data = json.dumps(dic)
    return HttpResponse(data, content_type='application/json')


@login_required
@transaction.atomic
def edit_user_profile(request):
    dic = {}
    if request.method == 'GET':
        return HttpResponse('Request is GET.')

    profile = get_object_or_404(Profile, user=request.user)
    profile_form = ProfileForm(request.POST, request.FILES, instance=profile)

    if not profile_form.is_valid():
        dic['type'] = 'error'
        dic['errors'] = [profile_form.errors[e] for e in profile_form.errors]
        data = json.dumps(dic)
        return HttpResponse(data, content_type='application/json')

    profile_form.save()

    dic['type'] = 'success'
    dic['profile'] = profile.to_json()
    data = json.dumps(dic)
    return HttpResponse(data, content_type='application/json')


@login_required
@transaction.atomic
def create_album(request, sound_id):
    dic = {}
    if request.method == 'GET':
        return HttpResponse('Request is GET.')

    new_album = Album(user=request.user)
    sound = get_object_or_404(Sound, id=sound_id)
    form = CreateAlbumForm(request.POST, request.FILES, instance=new_album)
    if not form.is_valid():
        dic['type'] = 'error'
        dic['errors'] = [form.errors[e] for e in form.errors]
        data = json.dumps(dic)
        return HttpResponse(data, content_type='application/json')

    form.save()
    sound.sound_albums.add(new_album)

    dic['type'] = 'success'
    dic['content'] = 'success set sound ' + sound.name + ' to album ' + new_album.name
    dic['new_album'] = new_album.to_json()
    dic['sound'] = sound.to_json()
    data = json.dumps(dic)
    return HttpResponse(data, content_type='application/json')


@login_required
@transaction.atomic
def create_sound(request):
    if request.method == 'GET':
        return HttpResponse('Request is GET.')
    # form_data = json.loads(request.body)
    new_sound = Sound(user=request.user)
    form = CreateSoundForm(request.POST, request.FILES, instance=new_sound)
    dic = {}
    if not form.is_valid():
        dic['type'] = 'error'
        dic['errors'] = [form.errors[e] for e in form.errors]
        data = json.dumps(dic)
        return HttpResponse(data, content_type='application/json')

    form.save()
    dic['type'] = 'success'
    dic['new_sound'] = new_sound.to_json()
    data = json.dumps(dic)
    return HttpResponse(data, content_type='application/json')


@login_required
@transaction.atomic
def create_music(request):
    if request.method == 'GET':
        return HttpResponse('Request is GET.')

    request_data = json.loads(request.body)
    new_music = Music(user=request.user)

    form = CreateMusicForm(request_data, instance=new_music)
    dic = {}

    if not form.is_valid():
        dic['type'] = 'error'
        dic['errors'] = [form.errors[e] for e in form.errors]
        data = json.dumps(dic)
        return HttpResponse(data, content_type='application/json')

    form.save()
    dic['type'] = 'success'
    dic['new_music'] = new_music.to_json()
    data = json.dumps(dic)
    return HttpResponse(data, content_type='application/json')


# def create_music(request):
#     if request.method == 'GET':
#         return HttpResponse('Request is GET.')

#     request_data = json.loads(request.body)
#     print request_data
#     music_name = request_data['name']
#     new_music = Music(user=request.user)

#     url = 'https://www.youtube.com/results?search_query=' + music_name
#     url_text = urllib2.urlopen(url).readlines()
#     for line in url_text:
#         # href="/watch?v=6KQPhoCICcs"
#         s = re.search(r'\"/watch\?v=\w*\"', line)
#         if s is not None:
#             watch_video = s.group()
#             start = watch_video.index('=') + 1
#             end = len(watch_video) - 1
#             watch_video = watch_video[start:end]
#             break

#     if watch_video is not None:
#         new_url = 'https://youtube.com/embed/' + watch_video + '?version=3' \
#                   '&autoplay=1&controls=0&showinfo=0&autohide=1' \
#                   '&loop=1&rel=0&modestbranding=0&playlist=' + watch_video;
#         music_post = request.POST.copy()
#         music_post['url'] = new_url
#         music_post['name'] = music_name

#         # img_url = 'http://img.youtube.com/vi/' + watch_video + '/0.jpg'
#         # image = urllib2.urlopen(img_url).read()
#         # new_music = Music(user=request.user, image=image)
#     form = CreateMusicForm(music_post, instance=new_music)
#     dic = {}
#     if not form.is_valid():
#         dic['type'] = 'error'
#         dic['errors'] = form.errors
#         data = json.dumps(dic)
#         return HttpResponse(data, content_type='application/json')

#     form.save()
#     dic['type'] = 'success'
#     dic['new_music'] = new_music.to_json()
#     data = json.dumps(dic)
#     return HttpResponse(data, content_type='application/json')



@login_required
@transaction.atomic
def delete_unused_sound(request, sound_id):
    dic = {}
    sound = get_object_or_404(Sound, id=sound_id)
    if sound.user == request.user:
        if sound.sound_albums.count() == 0:
            sound.delete()
            dic['type'] = 'success'
        else:
            request.user.user_sounds.remove(sound)
            dic['type'] = 'success'
    else:
        error = 'Cannot delete sound that is not belong to you.'
        dic['type'] = 'error'
        dic['errors'] = error

    dic['sound_id'] = sound_id
    data = json.dumps(dic)
    return HttpResponse(data, content_type='application/json')


@login_required
@transaction.atomic
def delete_unused_music(request, music_id):
    dic = {}
    music = get_object_or_404(Music, id=music_id)
    if music.user == request.user:
        if music.music_albums.count() == 0:
            music.delete()
            dic['type'] = 'success'
            dic['content'] = 'success delete music with name ' + music.name
        else:
            error = 'This music ' + music.name + ' is currently used by others, which cannot be deleted.'
            dic['type'] = 'error'
            dic['content'] = error
    else:
        error = 'Cannot delete music that is not belong to you.'
        dic['type'] = 'error'
        dic['content'] = error

    dic['music_id'] = music_id
    data = json.dumps(dic)
    return HttpResponse(data, content_type='application/json')


# @login_required
# @transaction.atomic
# def set_sound_in_album(request, album_id, sound_id):
#     dic = {}
#     album = get_object_or_404(Album, id=album_id)
#     sound = get_object_or_404(Sound, id=sound_id)
#     if album.user == request.user:
#         if album.sound == None:
#             sound.sound_albums.add(album)
#             dic['type'] = 'success'
#             dic['content'] = 'success set sound ' + sound.name + ' to album ' + album.name
#         else:
#             error = 'one sound already exist in this album.'
#             dic['type'] = 'error'
#             dic['content'] = error
#     else:
#         error = 'Cannot modify album that is not belong to you.'
#         dic['type'] = 'error'
#         dic['content'] = error
#     # return redirect(reverse('album_management'))
#
#     dic['sound_id'] = sound_id
#     data = json.dumps(dic)
#     return HttpResponse(data, content_type='application/json')


# Deperacated
@login_required
@transaction.atomic
def change_sound_in_album(request, album_id, sound_id):
    dic = {}
    album = get_object_or_404(Album, id=album_id)
    sound = get_object_or_404(Sound, id=sound_id)
    if album.user == request.user:
        if album.sound != None:
            old_sound = album.sound
            old_sound.sound_albums.remove(album)
            sound.sound_albums.add(album)
            dic['type'] = 'success'
            dic['content'] = 'success change sound ' + sound.name + ' to album ' + album.name
        else:
            error = 'cannot change sound in album, since this album sound is not none'
            dic['type'] = 'error'
            dic['content'] = error
    else:
        error = 'Cannot modify album that is not belong to you.'
        dic['type'] = 'error'
        dic['content'] = error
    # return redirect(reverse('album_management'))

    dic['sound_id'] = sound_id
    data = json.dumps(dic)
    return HttpResponse(data, content_type='application/json')


@login_required
@transaction.atomic
def add_music_in_album(request, album_id, music_id):
    dic = {}
    album = get_object_or_404(Album, id=album_id)
    music = get_object_or_404(Music, id=music_id)
    if album.user == request.user:
        album.musics.add(music)
        dic['type'] = 'success'
        dic['content'] = 'success add music ' + music.name + ' to album ' + album.name
    else:
        error = 'Cannot modify album that is not belong to you.'
        dic['type'] = 'error'
        dic['content'] = error

    dic['music'] = music.to_json()
    data = json.dumps(dic)
    return HttpResponse(data, content_type='application/json')


@login_required
@transaction.atomic
def delete_music_in_album(request, album_id, music_id):
    dic = {}
    album = get_object_or_404(Album, id=album_id)
    music = get_object_or_404(Music, id=music_id)
    if album.user == request.user:
        album.musics.remove(music)
        dic['type'] = 'success'
        dic['content'] = 'success delete music ' + music.name + ' from album ' + album.name
    else:
        error = 'Cannot modify album that is not belong to you.'
        dic['type'] = 'error'
        dic['errors'] = error
    dic['music'] = music.to_json()
    data = json.dumps(dic)
    return HttpResponse(data, content_type='application/json')


@login_required
def delete_user_album(request, album_id):
    dic = {}
    user = request.user
    album = get_object_or_404(Album, id=album_id)
    if album.user == user:
        album.delete()
        dic['type'] = 'success'
    else:
        error = 'Cannot modify album that is not belong to you.'
        dic['type'] = 'error'
        dic['errors'] = error
    data = json.dumps(dic)
    return HttpResponse(data, content_type='application/json')


@login_required
@transaction.atomic
def add_comment(request, album_id):
    dic = {}
    if request.method == 'GET':
        return HttpResponse('Request is GET')

    album = get_object_or_404(Album, id=album_id)
    request_data = json.loads(request.body)

    if not request_data or not request_data['comment']:
        dic['type'] = 'error'
        dic['errors'] = 'comment content invalid'
        data = json.dumps(dic)
        return HttpResponse(data, content_type='application/json')

    content = request_data['comment']
    new_comment = Comment(album=album, user=request.user, content=content)  # add some 'latitude' 'longitude' maybe
    # form = AddCommentForm(request.POST, instance=new_comment)
    new_comment.save()
    dic['type'] = 'success'
    dic['comment'] = new_comment.to_json()
    data = json.dumps(dic)
    return HttpResponse(data, content_type='application/json')


@login_required
@transaction.atomic
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    dic = {}
    if comment.user == request.user:
        comment.delete()
        dic['type'] = 'success'
        dic['comment_id'] = comment_id
        # no need, since already set blank=True, null=True, on_delete=models.SET_NULL
        # album = comment.album
        # album.album_comments.remove(comment)
    else:
        dic['type'] = 'error'
        dic['errors'] = "Cannot delete comment that is not belong to you."
    data = json.dumps(dic)
    return HttpResponse(data, content_type='application/json')


@login_required
@transaction.atomic
def favorite(request, album_id):
    dic = {}
    album = get_object_or_404(Album, id=album_id)
    current_user_profile = request.user.user_profile
    if current_user_profile.favorites.filter(id=album.id).count() > 0:
        dic['type'] = 'error'
        dic['errors'] = 'Duplicate favorite.'
    else:
        current_user_profile.favorites.add(album)
        dic['type'] = 'success'
        dic['album'] = album.to_json()
    data = json.dumps(dic)
    return HttpResponse(data, content_type='application/json')


@login_required
@transaction.atomic
def unfavorite(request, album_id):
    dic = {}
    user = request.user
    album = get_object_or_404(Album, id=album_id)
    user.user_profile.favorites.remove(album)
    dic['type'] = 'success'
    dic['album'] = album.to_json()
    data = json.dumps(dic)
    return HttpResponse(data, content_type='application/json')

    # @login_required
    # def getFavoriteCount(request, album_id):
    # album = get_object_or_404(Album, id=album_id)
