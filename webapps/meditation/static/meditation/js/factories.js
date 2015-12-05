var app = angular.module('factoriesModule', []);

// Factories
app.factory('userFactory', function ($http) {
    var factory = {};

    factory.get_user = function () {
        return $http.get('/meditation/get-user');
    };

    factory.get_user_albums = function () {
        return $http.get('/meditation/get-user-albums');
    };

    factory.get_user_sounds = function () {
        return $http.get('/meditation/get-user-sounds');
    };

    factory.get_user_musics = function () {
        return $http.get('/meditation/get-user-musics');
    };

    factory.get_user_favorite_albums = function () {
        return $http.get('/meditation/get-user-favorite-albums');
    };

    // get other user's album/sound/music by id
    factory.get_other_albums = function (user_id) {
        return $http.get('/meditation/get-others-albums/' + user_id);
    };

    factory.get_other_sounds = function (user_id) {
        return $http.get('/meditation/get-others-sounds/' + user_id);
    };

    factory.get_other_favorite_albums = function (user_id) {
        return $http.get('/meditation/get-others-favorite-albums/' + user_id);
    };

    factory.create_sound = function (sound) {
        return $http.post('/meditation/create-sound', sound);
    };

    factory.create_music = function (music_name, music_url) {
        return $http.post('/meditation/create-music', {'name': music_name, 'url': music_url});
    };

    //factory.create_album = function (album) {
    //    return $http.post('/meditation/create-album', album);
    //};

    factory.get_sound_id = function (sound_id) {
        return $http.get('/meditation/create-album/' + sound_id);
    };

    factory.delete_music_in_album = function (album_id, music_id) {
        return $http.get('/meditation/delete-music-in-album/' + album_id + '/' + music_id);
    };

    factory.delete_user_album = function (album_id) {
        return $http.get('/meditation/delete-user-album/' + album_id);
    };

    factory.delete_unused_sound = function (sound_id) {
        return $http.get('/meditation/delete-unused-sound/' + sound_id);
    };

    factory.delete_unused_music = function (music_id) {
        return $http.get('/meditation/delete-unused-music/' + music_id);
    };

    factory.add_music_in_album = function (album_id, music_id) {
        return $http.get('/meditation/add-music-in-album/' + album_id + '/' + music_id);
    };

    factory.add_comment = function (album_id, comment) {
        console.log(comment);
        return $http.post('/meditation/add-comment/' + album_id, {'comment': comment});
    };

    factory.delete_comment = function (comment_id) {
        return $http.get('/meditation/delete-comment/' + comment_id);
    };

    factory.favorite = function (album_id) {
        return $http.get('/meditation/favorite/' + album_id);
    };

    factory.unfavorite = function (album_id) {
        return $http.get('/meditation/unfavorite/' + album_id);
    };

    //factory.set_sound_in_album = function (album_id, sound_id) {
    //    return $http.get('/meditation/set-sound-in-album/' + album_id + '/' + sound_id);
    //};

    return factory;
});

app.factory('allFactory', function ($http) {
    var factory = {};

    // factory.get_all_albums = function () {
    //     return $http.get('/meditation/get-all-albums');
    // };

    factory.get_all_sounds = function () {
        return $http.get('/meditation/get-all-sounds');
    };

    factory.get_albums_by_sound = function (id) {
        return $http.get('/meditation/get-albums/' + id);
    };

    factory.get_sound_content = function (id) {
        return $http.get('/meditation/get-sound-content/' + id);
    };


    return factory;
});