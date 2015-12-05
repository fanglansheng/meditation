from django.conf.urls import url
from meditation.forms import MyAuthenticationForm

urlpatterns = [
    ## view.py
    url(r'^$', 'meditation.views.home', name='home'),
    url(r'^home-login$', 'meditation.views.home_login', name='login_home'),
    url(r'^album-management$', 'meditation.views.album_management', name='album_management'),

    # users personal profile
    url(r'^user-profile/(?P<user_id>[0-9]+)$', 'meditation.views.user_profile', name='user_profile'),
    url(r'^get-partial-html/(?P<urlPath>.*)$','meditation.views.getPartialHtml', name='getPartialHtml'),


    ## view_auth.py
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'meditation/home.html', 'authentication_form': MyAuthenticationForm}, name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^login-auth$', 'meditation.views_auth.login_auth', name='login_auth'),

    # register with email confirmation
    url(r'^register-info/(?P<username>\w+)$', 'meditation.views_auth.register_info', name='register_info'),
    url(r'^register$', 'meditation.views_auth.register', name='register'),
    url(r'^confirm-register/(?P<username>.*)/(?P<token>.*)$', 'meditation.views_auth.confirm_register', name='confirm_register'),

    # reset password without logging in
    url(r'^reset-password-info/(?P<username>\w+)$', 'meditation.views_auth.reset_password_info', name='reset_password_info'),
    url(r'^reset-password-email$', 'meditation.views_auth.reset_password_email', name='reset_password_email'),
    url(r'^confirm-reset-password-email/(?P<username>.*)/(?P<password_enc>.*)/(?P<token>.*)$', 'meditation.views_auth.confirm_reset_password_email', name='confirm_reset_password_email'),

    # change password when logged in
    url(r'^change-password-inner$', 'meditation.views_auth.change_password_inner', name='change_password_inner'),


    ## views_get_media.py
    url(r'^get-user-profile/(?P<user_id>[0-9]+)$', 'meditation.views_logic.get_user_profile', name='get_user_profile'),
    url(r'^edit-user-profile$', 'meditation.views_logic.edit_user_profile', name='edit_user_profile'),

    # create or delete thing from database, delete can only happen on the user who create that thing
    # create album is to create an empty album, can later set sound and add music
    url(r'^create-album/(?P<sound_id>[0-9]+)$', 'meditation.views_logic.create_album', name='create_album'),
    url(r'^create-sound$', 'meditation.views_logic.create_sound', name='create_sound'),
    url(r'^create-music$', 'meditation.views_logic.create_music', name='create_music'),

    url(r'^delete-user-album/(?P<album_id>[0-9]+)$', 'meditation.views_logic.delete_user_album', name='delete_user_album'),
    url(r'^delete-unused-sound/(?P<sound_id>[0-9]+)$', 'meditation.views_logic.delete_unused_sound', name='delete_unused_sound'),
    url(r'^delete-unused-music/(?P<music_id>[0-9]+)$', 'meditation.views_logic.delete_unused_music', name='delete_unused_music'),

    # change relations of things
    # url(r'^set-sound-in-album/(?P<album_id>[0-9]+)/(?P<sound_id>[0-9]+)$', 'meditation.views.set_sound_in_album', name='set_sound_in_album'),
    url(r'^change-sound-in-album/(?P<album_id>[0-9]+)/(?P<sound_id>[0-9]+)$', 'meditation.views_logic.change_sound_in_album', name='change_sound_in_album'),
    url(r'^add-music-in-album/(?P<album_id>[0-9]+)/(?P<music_id>[0-9]+)$', 'meditation.views_logic.add_music_in_album', name='add_music_in_album'),
    url(r'^delete-music-in-album/(?P<album_id>[0-9]+)/(?P<music_id>[0-9]+)$', 'meditation.views_logic.delete_music_in_album', name='delete_music_in_album'),

    # add or delete comment
    url(r'^add-comment/(?P<album_id>[0-9]+)$', 'meditation.views_logic.add_comment', name='add_comment'),
    url(r'^delete-comment/(?P<comment_id>[0-9]+)$', 'meditation.views_logic.delete_comment', name='delete_comment'),

    # add or delete facorite, like follow, others albums
    url(r'^favorite/(?P<album_id>[0-9]+)$', 'meditation.views_logic.favorite', name='favorite'),
    url(r'^unfavorite/(?P<album_id>[0-9]+)$', 'meditation.views_logic.unfavorite', name='unfavorite'),


    ## views_get_media.py
    # get image
    url(r'^get-user-image/(?P<user_id>[0-9]+)', 'meditation.views_get_media.get_user_image', name='get_user_image'),
    url(r'^get-album-image/(?P<album_id>[0-9]+)', 'meditation.views_get_media.get_album_image', name='get_album_image'),
    url(r'^get-sound-image/(?P<sound_id>[0-9]+)', 'meditation.views_get_media.get_sound_image', name='get_sound_image'),
    url(r'^get-music-image/(?P<music_id>[0-9]+)', 'meditation.views_get_media.get_music_image', name='get_music_image'),

    # get media content
    url(r'^get-sound-content/(?P<sound_id>[0-9]+)', 'meditation.views_get_media.get_sound_content', name='get_sound_content'),
    url(r'^get-music-content/(?P<music_id>[0-9]+)', 'meditation.views_get_media.get_music_content', name='get_music_content'),


    ## views_get_model_json.py
    # urls for getting data from front end
    url(r'^get-all-albums$','meditation.views_get_model_json.get_all_albums', name='get_all_albums'),
    url(r'^get-all-sounds$','meditation.views_get_model_json.get_all_sounds', name='get_all_sounds'),
    url(r'^get-all-musics$','meditation.views_get_model_json.get_all_musics', name='get_all_musics'),

    # get albums which has selected sound
    url(r'^get-albums/(?P<sound_id>[0-9]+)$','meditation.views_get_model_json.get_albums', name='get_albums_by_sound'),
    url(r'^get-sound-id/(?P<sound_id>[0-9]+)$','meditation.views_get_model_json.get_sound_id', name='get_sound_id'),

    # urls for getting information for certain user
    url(r'^get-user$','meditation.views_get_model_json.get_user', name='get_user'),
    url(r'^get-user-albums$','meditation.views_get_model_json.get_user_albums', name='get_user_albums'),
    url(r'^get-user-sounds$','meditation.views_get_model_json.get_user_sounds', name='get_user_sounds'),
    url(r'^get-user-musics$','meditation.views_get_model_json.get_user_musics', name='get_user_musics'),
    url(r'^get-user-favorite-albums$','meditation.views_get_model_json.get_user_favorite_albums', name='get_user_favorite_albums'),

    url(r'^get-others-albums/(?P<user_id>[0-9]+)$','meditation.views_get_model_json.get_others_albums'),
    url(r'^get-others-sounds/(?P<user_id>[0-9]+)$','meditation.views_get_model_json.get_others_sounds'),
    url(r'^get-others-favorite-albums/(?P<user_id>[0-9]+)$','meditation.views_get_model_json.get_others_favorite_albums'),


    ## views_plurin.py
    url(r'^create-sound-plugin$', 'meditation.views_plugin.create_sound_plugin', name='create_sound_plugin'),
    url(r'^create-music-plugin$', 'meditation.views_plugin.create_music_plugin', name='create_music_plugin'),
]
