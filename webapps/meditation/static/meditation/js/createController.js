var app = angular.module('createControllerModule', []);

app.controller('createController', function ($scope, Upload, userFactory) {
    $scope.createAlbumError;
    $scope.createSoundError;
    $scope.createMusicError;

    $scope.create_sound = function () {
        console.log($scope.sound_creation_data);
        if ($scope.sound_creation_data) {
            if (!$scope.sound_creation_data.name) {
                $scope.createSoundError = 'Name field is required to create a sound.';
            } else if (!$scope.sound_creation_data.url && !$scope.sound_creation_data.content) {
                $scope.createSoundError = 'Either url or content is required to create a sound.';
            } else {
                Upload.upload({
                    url: '/meditation/create-sound',
                    data: {
                        'name': $scope.sound_creation_data.name,
                        'url': $scope.sound_creation_data.url,
                        'content': $scope.sound_creation_data.content,
                        'image': $scope.sound_creation_data.image
                    }
                }).success(function (data) {
                    if (data.type == 'error') {
                        $scope.status = data.errors.join(" And ");
                        $scope.createSoundError = data.errors.join(" And ");
                        $scope.showStatus();
                    } else {
                        //$scope.status = 'success';
                        var new_sound = data.new_sound;

                        // $scope.all_sounds.push(new_sound);
                        // $scope.user_sounds.push(new_sound);

                        $('#create_sound_form').get(0).reset();

                        $scope.setCurrentSound(new_sound);
                        // add new sound to mainController all_sound
                        var soundList = $scope.getSoundList();
                        soundList.push(new_sound);
                        $scope.setSoundList(soundList);

                        var userSound = $scope.getUserSounds();
                        userSound.push(new_sound);
                        $scope.setUserSounds(userSound);

                        $scope.updateSelfProfile();

                        //$scope.status = 'success create sound' + new_sound.name;
                        $scope.createSoundError = 'success create sound' + new_sound.name;
                        setTimeout(function () {
                            $scope.createSoundError = '';
                            $('#c-sound-popup').modal('hide');
                        }, 1000);
                    }
                });
            }
        } else {
            $scope.createSoundError = 'Please fill in required fields to create a sound.';
        }
    };

    // false to show the error info label
    $scope.notEmptyList = true;
    $scope.create_music = function () {

        // check is form's album list is empty
        $scope.notEmptyList = false;

        var userAlbums = $scope.getUserAlbums();
        for (var i = 0; i < userAlbums.length; i++) {
            //console.log($scope.user_albums[i].added);
            $scope.notEmptyList = $scope.notEmptyList || userAlbums[i].added;
        }

        // prevent create music if user didn't choose which albums to add to.
        if ($scope.notEmptyList == false) return;

        // send create music request to server
        if ($scope.music_creation_data) {
            if ($scope.music_creation_data.name && $scope.music_creation_data.url) {

                userFactory.create_music($scope.music_creation_data.name, $scope.music_creation_data.url)
                    .success(function (data) {
                         if (data.type == 'error') {
                            //$scope.status = data.errors.join(" And ");
                            $scope.createMusicError = data.errors.join(" And ");
                        } else {
                            var new_music = data.new_music;

                            $('#create_music_form').get(0).reset();

                            // add mew music to selected albums
                            for (var i = 0; i < userAlbums.length; i++) {
                                if (userAlbums[i].added) {

                                    addMusicInTimeOut(userAlbums[i], new_music);
                                    //$scope.add_music_in_album(userAlbums[i], new_music);


                                    // add new music to currenAlbum
                                    // var currentAlbum = $scope.getCurrentAlbum();
                                    // if (userAlbums[i].id == currentAlbum.id) {
                                    //     currentAlbum.musics.push(new_music);
                                    //     $scope.setCurrentAlbum(currentAlbum);
                                    // }
                                    var currentAlbum = $scope.getCurrentAlbum();
                                    if (userAlbums[i].id == currentAlbum.id) {
                                        $scope.setCurrentAlbum(userAlbums[i]);
                                    }
                                }
                            }

                            $scope.updateSelfProfile();

                            //$scope.status = 'success create music' + new_music.name;
                            $scope.createMusicError = 'success create music' + new_music.name;
                            setTimeout(function () {
                                $scope.createMusicError = '';
                                $('#c-music-popup').modal('hide');
                            }, 1000);
                        }
                    })
                    .error(function (error) {
                        $scope.status = 'Unable to create music, please refresh and try again. Error message: ' + error.message;
                        $scope.showStatus();
                    });

            } else {
                $scope.createMusicError = 'Please fill in name and url to create a music.';
            }
        } else {
            $scope.createMusicError = 'Please fill in required fields to create a music.';
        }
    };

    $scope.create_album = function (sound) {
        if ($scope.album_creation_data) {
            if ($scope.album_creation_data.name) {
                Upload.upload({
                    url: '/meditation/create-album/' + sound.id,
                    data: {
                        'name': $scope.album_creation_data.name,
                        'image': $scope.album_creation_data.image,
                        'description' : $scope.album_creation_data.description
                    }
                }).success(function (data) {
                    if (data.type == 'error') {
                        //$scope.status = data.errors.join(" And ");
                        $scope.createAlbumError = data.errors.join(" And ");
                    } else {
                        if ($scope.currentSound && $scope.currentAlbum) {
                            var new_album = data.new_album;
                            var new_sound = data.sound;

                            var userAlbums = $scope.getUserAlbums();
                            userAlbums.push(new_album);
                            $scope.setUserAlbums(userAlbums);

                            var albumList = $scope.getAlbumList();
                            albumList.push(new_album);
                            $scope.setAlbumList(albumList);

                            $scope.updateSelfProfile();

                            $('#create_album_form').get(0).reset();
                            $scope.createAlbumError = 'success create album: ' + new_album.name + ', and set sound: ' + new_sound.name;
                            //$scope.status = 'success create album: ' + new_album.name + ', and set sound: ' + new_sound.name;
                            setTimeout(function () {
                                $scope.createAlbumError = '';
                                $('#c-album-popup').modal('hide');
                            }, 1000);
                        } else {
                            $scope.status = 'Unable to create album, please refresh and try again. Error message: ' + data.errors;
                        }
                    }

                    $scope.showStatus();
                });
            } else {
                $scope.createAlbumError = 'Please fill in album name to create an album.';
            }
        } else {
            $scope.createAlbumError = 'Please fill in required fields to create an album.';
        }
    };

    function addMusicInTimeOut (userAlbumTimeOut, newMusicTimeOut) {
        setTimeout(function() {
            $scope.add_music_in_album(userAlbumTimeOut, newMusicTimeOut);
        }, 100);
    }
});