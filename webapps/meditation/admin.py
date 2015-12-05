from django.contrib import admin

from .models import Album, Sound, Music, Profile, Comment, Recommendation

admin.site.register(Album)
admin.site.register(Sound)
admin.site.register(Music)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Recommendation)
