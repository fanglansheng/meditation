from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max


def user_to_json(user):
    dic = dict()
    if user is None:
        return dic
    dic['id'] = user.id
    dic['username'] = user.username
    dic['password'] = user.password
    # dic['profile'] = user.user_profile.to_json()
    # dic['recommendations'] = [r.to_json() for r in user.user_recommendation.all()]
    # dic['sound'] =[s.to_json() for s in user.user_sounds.all()]
    return dic


class Sound(models.Model):
    user = models.ForeignKey(User, related_name='user_sounds', blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=42)
    url = models.URLField(max_length=200, default='', blank=True)
    datetime = models.DateTimeField(auto_now=True)
    content = models.FileField(upload_to='meditation/sound/', blank=True, null=True)
    image = models.ImageField(upload_to='meditation/sound/', default='meditation/sound/no-sound-image.jpg', blank=True)

    def to_json(self):
        dic = dict()
        dic['user'] = user_to_json(self.user)
        dic['id'] = self.id
        dic['name'] = self.name
        dic['url'] = self.url
        dic['datetime'] = self.datetime.isoformat()
        dic['content'] = self.content.url if hasattr(self.content, 'url') and self.content.url is not None else ''
        dic['image'] = self.image.url
        return dic

    def __unicode__(self):
        return self.name + str(self.datetime)


class Music(models.Model):
    user = models.ForeignKey(User, related_name='user_musics', blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=42)
    url = models.URLField(max_length=200, default='')
    datetime = models.DateTimeField(auto_now=True)
    content = models.FileField(upload_to='meditation/music/', blank=True, null=True)
    image = models.ImageField(upload_to='meditation/music/', default='meditation/music/no-music-image.jpg', blank=True)

    def to_json(self):
        dic = dict()
        dic['user'] = user_to_json(self.user)
        dic['id'] = self.id
        dic['name'] = self.name
        dic['url'] = self.url
        dic['datetime'] = self.datetime.isoformat()
        dic['content'] = self.content.url if hasattr(self.content, 'url') and self.content.url is not None else ''
        dic['image'] = self.image.url
        return dic

    def __unicode__(self):
        return self.name + str(self.datetime)


class Album(models.Model):
    user = models.ForeignKey(User, related_name='user_albums', blank=True, null=True, on_delete=models.SET_NULL)
    sound = models.ForeignKey(Sound, related_name='sound_albums', blank=True, null=True, on_delete=models.SET_NULL)
    musics = models.ManyToManyField(Music, related_name='music_albums', blank=True)
    name = models.CharField(max_length=42)
    datetime = models.DateTimeField(auto_now=True)
    description = models.TextField(max_length=200, default="", blank=True)
    image = models.ImageField(upload_to='meditation/album/', default='meditation/album/no-album-image.jpg', blank=True)

    def to_json(self):
        dic = dict()
        dic['user'] = user_to_json(self.user)
        dic['id'] = self.id
        dic['sound'] = self.sound.to_json() if self.sound is not None else ''
        dic['musics'] = [m.to_json() for m in self.musics.all()]
        dic['name'] = self.name
        dic['datetime'] = self.datetime.isoformat()
        dic['image'] = self.image.url
        dic['comment'] = [c.to_json() for c in self.album_comments.all()]
        dic['description'] = self.description
        dic['favorite'] = len(self.user_favorite_albums.all())
        return dic

    def getFavoriteCount(self):
        return len(self.user_favorite_albums.all())

    @staticmethod
    def get_max_id():
        return Album.objects.all().aggregate(Max('id'))['id__max'] or 0

    def __unicode__(self):
        return self.name + str(self.datetime)


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile', blank=True, null=True, on_delete=models.SET_NULL)
    favorites = models.ManyToManyField(Album, related_name='user_favorite_albums', blank=True)
    first_name = models.CharField(max_length=20, default="", blank=True)
    last_name = models.CharField(max_length=20, default="", blank=True)
    bio = models.TextField(max_length=1000, default="", blank=True)
    image = models.ImageField(upload_to='meditation/user/', default='meditation/user/no-user-image.jpg', blank=True)

    def to_json(self):
        dic = dict()
        dic['user'] = user_to_json(self.user)
        dic['id'] = self.id
        dic['favorites'] = [a.to_json() for a in self.favorites.all()]
        dic['first_name'] = self.first_name
        dic['last_name'] = self.last_name
        dic['bio'] = self.bio
        dic['image'] = self.image.url
        return dic


    def __unicode__(self):
        return self.first_name + self.last_name + self.bio


class Comment(models.Model):
    user = models.ForeignKey(User, related_name='user_comments', blank=True, null=True, on_delete=models.SET_NULL)
    album = models.ForeignKey(Album, related_name='album_comments', blank=True, null=True, on_delete=models.SET_NULL)
    datetime = models.DateTimeField(auto_now=True)
    content = models.TextField(max_length=200)

    def to_json(self):
        dic = dict()
        dic['user'] = user_to_json(self.user)
        dic['id'] = self.id
        # dic['album'] = self.album.to_json()
        dic['datetime'] = self.datetime.isoformat()
        dic['content'] = self.content
        return dic

    def __unicode__(self):
        return self.content + str(self.datetime)


class Recommendation(models.Model):
    user = models.ForeignKey(User, related_name='user_recommendation', blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=42, default='', blank=True)
    content = models.CharField(max_length=3000, default='', blank=True)

    def to_json(self):
        dic = dict()
        dic['user'] = user_to_json(self.user)
        dic['id'] = self.id
        dic['name'] = self.name
        dic['content'] = self.content
        return dic

    def __unicode__(self):
        return self.name + self.content

