from django.test import TestCase, Client
from meditation.models import *


class TodoListModelsTest(TestCase):
    def test_simple_add(self):
        user = User(username='test', password='test')
        user.save()

        self.assertTrue(Sound.objects.all().count() == 0)
        new_sound = Sound(user=user, name='test')
        new_sound.save()
        self.assertTrue(Sound.objects.all().count() == 1)

        self.assertTrue(Music.objects.all().count() == 0)
        new_music = Music(user=user, name='test')
        new_music.save()
        self.assertTrue(Music.objects.all().count() == 1)

        self.assertTrue(Album.objects.all().count() == 0)
        new_album = Album(user=user, name='test')
        new_album.save()
        self.assertTrue(Album.objects.all().count() == 1)

        self.assertTrue(Profile.objects.all().count() == 0)
        new_profile = Profile(user=user)
        new_profile.save()
        self.assertTrue(Profile.objects.all().count() == 1)

        self.assertTrue(Comment.objects.all().count() == 0)
        new_comment = Comment(user=user)
        new_comment.save()
        self.assertTrue(Comment.objects.all().count() == 1)

        self.assertTrue(Recommendation.objects.all().count() == 0)
        new_recommendation = Recommendation(user=user, name='test')
        new_recommendation.save()
        self.assertTrue(Recommendation.objects.all().count() == 1)


class FunctionTest(TestCase):
    def test_create_album(self):
        client = Client()
        self.assertTrue(Album.objects.count() == 0)
        name = 'This is the test album name'
        response = client.post('/meditation/create-album', {'name': name, 'image': 'test.jpg'})
        self.assertTrue(Album.objects.count() == 1)
        # self.assertTrue(response.content.find(name.encode()) >= 0)



