var app = angular.module('mainControllerModule', []);

app.controller('mainController', function ($http, $scope, allFactory, userFactory) {

    $scope.status;

    // all sounds in the website
    $scope.all_sounds;
    // albums of current sound
    $scope.albumList;

    // user selected album/sound/music
    $scope.currentAlbum;
    $scope.currentSound;
    $scope.currentMusic;

    // logged in user's data
    $scope.user_albums;
    $scope.user_sounds;
    $scope.user_musics;
    $scope.user_favorite_albums;

    $scope.currentUser;
    $scope.otherUser;

    // for display and update img in nav bar
    $scope.image = {};
    $scope.image.imgSrc;

    init_all_content();

    init_user_content();

    // getter and setter functions
    $scope.setAlbumList = function (newList) {
        $scope.albumList = newList;
    };

    $scope.getAlbumList = function () {
        return $scope.albumList;
    };

    $scope.setSoundList = function (newList) {
        $scope.all_sounds = newList;
    };

    $scope.getSoundList = function () {
        return $scope.all_sounds;
    };

    $scope.setOtherUser = function (user) {
        $scope.otherUser = user;
    };

    $scope.setCurrentAlbum = function (newAlbum) {
        $scope.currentAlbum = newAlbum;
        //console.log("currentAlbum: ", $scope.currentAlbum.name);
        //    You can add some css to the selected album item
    };

    $scope.getCurrentAlbum = function () {
        return $scope.currentAlbum;
    };

    $scope.setCurrentSound = function (newSound) {
        $scope.currentSound = newSound;
        //$scope.status = 'Current sound is ' + newSound.name;
        //    You can add some css to the selected album item
    };

    $scope.setCurrentMusic = function (newMusic) {
        $scope.currentMusic = newMusic;
    };

    $scope.getUserAlbums = function () {
        return $scope.user_albums;
    };

    $scope.setUserAlbums = function (albums) {
        $scope.user_albums = albums;
    };

    $scope.getUserSounds = function(){
        return $scope.user_sounds;
    };

    $scope.setUserSounds = function(sounds){
        $scope.user_sounds = sounds;
    };

    $scope.getUserFavoriteAlbums = function(){
        return $scope.user_favorite_albums;
    };

    $scope.setUserFavoriteAlbums = function(favorites){
        $scope.user_favorite_albums = favorites;
    };

    // datas in profile page
    $scope.profileSounds;
    $scope.profileFavorites;
    $scope.profileAlbums;

    $scope.setProfileSounds = function(sounds){
        $scope.profileSounds = sounds;
    };

    $scope.getProfileSounds = function(){
        return $scope.profileSounds;
    };

    $scope.setProfileAlbums = function(albums){
        $scope.profileAlbums = albums;
    };

    $scope.getProfileAlbums = function(){
        return $scope.profileAlbums;
    };

    $scope.setProfileFavorites = function(favorites){
        $scope.profileFavorites = favorites;
    };
    
    $scope.getProfileFavorites = function(){
        return $scope.profileFavorites;
    };

    $scope.isHome = true;
    $scope.setIsHome = function(home){
        $scope.isHome = home; 
    };
    // update profile data in when updating user info
    $scope.updateSelfProfile = function () {
        console.log($scope.otherUser, $scope.currentUser);
        if ($scope.currentUser && $scope.otherUser) {
            if ($scope.otherUser.id == $scope.currentUser.id) {
                $scope.profileSounds = $scope.user_sounds;
                $scope.profileFavorites = $scope.user_favorite_albums;
                $scope.profileAlbums = $scope.user_albums;
            }
        }
    };

    $scope.favorite = function (album) {
        // don't allow to add favorite if user is not logged in
        if ($scope.currentUser == undefined) {
            return;
        }

        if (!$scope.checkFavorite(album)) {
            $scope.updateSelfProfile();
            userFactory.favorite(album.id)
                .success(function (data) {
                    if (data.type === 'success') {
                        console.log($scope.user_favorite_albums);
                        console.log($scope.user_albums);
                        album.favorite++;
                        console.log(album.favorite);
                        if ($scope.user_favorite_albums.indexOf(album) == -1) {
                            $scope.user_favorite_albums.push(album);
                        }                        

                        $scope.updateSelfProfile();

                        $scope.status = 'Success add to user favorite album: ' + album.name;
                    } else {
                        $scope.status = 'Unable to add favorite, please refresh and try again. Error message: ' + data.errors;
                    }
                })
                .error(function (error) {
                    $scope.status = 'Unable to add favorite, please refresh and try again. Error message: ' + error.message;
                });

            $scope.showStatus();
        }
        else {
            $scope.unfavorite(album);
        }

    };

    $scope.unfavorite = function (album) {
        if (confirm("Confirm that you want to remove " + album.name + " from your favorite albums?")) {
            userFactory.unfavorite(album.id)
                .success(function (data) {
                    if (data.type === 'success') {
                        album.favorite--;
                        
                        for (var i = $scope.user_favorite_albums.length - 1; i >= 0; i--) {
                            if ($scope.user_favorite_albums[i].id === album.id) {
                                $scope.user_favorite_albums.splice(i, 1);
                                break;
                            }
                        }

                        // for(var i = 0; i < $scope.user_albums.length; i++){
                        //     console.log(album.id,$scope.user_albums[i].id);
                        //     if(album.id == $scope.user_albums[i].id){
                        //         $scope.user_albums[i].favorite--;
                        //     }
                        // }

                        $scope.updateSelfProfile();

                        $scope.status = 'Success remove from user favorite album: ' + album.name;
                    } else {
                        $scope.status = 'Unable to delete user album, please refresh and try again. Error message: ' + data.errors;
                    }
                })
                .error(function (error) {
                    $scope.status = 'Unable to delete user album, please refresh and try again. Error message: ' + error.message;
                });
            $scope.showStatus();
        }
    };

    $scope.add_comment = function (album, newComment) {
        userFactory.add_comment(album.id, newComment)
            .success(function (data) {
                if (data.type === 'success') {
                    var comment = data.comment;
                    //album.comment.push(comment);

                    for (var i = $scope.profileFavorites.length - 1; i >= 0; i--) {
                        if ($scope.profileFavorites[i].id === album.id) {
                            var favoriteAlbum = $scope.profileFavorites[i];
                            favoriteAlbum.comment.push(comment);
                            break;
                        }
                    }

                    for (var i = $scope.profileAlbums.length - 1; i >= 0; i--) {
                        if ($scope.profileAlbums[i].id === album.id) {
                            var profileAlbum = $scope.profileAlbums[i];
                            profileAlbum.comment.push(comment);
                            break;
                        }
                    }

                    $scope.newComment = '';
                    $scope.status = 'Success add comment to album: ' + album.name;
                } else {
                    $scope.status = 'Unable to add comment, please refresh and try again. Error message: ' + data.errors;
                }
                $scope.showStatus();
            })
            .error(function (error) {
                $scope.status = 'Unable to add comment, please refresh and try again. Error message: ' + error.message;
                $scope.showStatus();
            });

    };

    $scope.delete_comment = function (album, comment) {
        if (confirm("Confirm that you want to delete this comment? Note that you can not delete others' comment.")) {
            userFactory.delete_comment(comment.id)
                .success(function (data) {
                    if (data.type === 'success') {
                        //for (var i = album.comment.length - 1; i >= 0; i--) {
                        //    if (album.comment[i].id === comment.id) {
                        //        album.comment.splice(i, 1);
                        //        break;
                        //    }
                        //}

                        for (var i = $scope.profileFavorites.length - 1; i >= 0; i--) {
                            if ($scope.profileFavorites[i].id === album.id) {
                                var favoriteAlbum = $scope.profileFavorites[i];
                                for (var i = favoriteAlbum.comment.length - 1; i >= 0; i--) {
                                    if (favoriteAlbum.comment[i].id === comment.id) {
                                        favoriteAlbum.comment.splice(i, 1);
                                        break;
                                    }
                                }
                            }
                        }

                        for (var i = $scope.profileAlbums.length - 1; i >= 0; i--) {
                            if ($scope.profileAlbums[i].id === album.id) {
                                var profileAlbum = $scope.profileAlbums[i];
                                for (var i = profileAlbum.comment.length - 1; i >= 0; i--) {
                                    if (profileAlbum.comment[i].id === comment.id) {
                                        profileAlbum.comment.splice(i, 1);
                                        break;
                                    }
                                }
                            }
                        }

                        $scope.status = 'Successful delete comment from album' + album.name;
                    } else {
                        $scope.status = 'Unable to delete comment, please refresh and try again. Error message: ' + data.errors;
                    }
                    $scope.showStatus();
                })
                .error(function (error) {
                    $scope.status = 'Unable to delete comment, please refresh and try again. Error message: ' + error.message;
                    $scope.showStatus();
                });
        }
    };

    $scope.add_music_in_album = function (album, music) {
        userFactory.add_music_in_album(album.id, music.id)
            .success(function (data) {
                
                if (data.type === 'success') {
                    album.musics.push(music);
                    $scope.status = 'Success add music' + music.name + ' to album ' + album.name;
                    //console.log("!!add"+album.name);

                    allFactory.get_albums_by_sound($scope.currentSound.id)
                        .success(function (data) {
                            console.log(data);
                            $scope.albumList = data;
                        });

                } else {
                    $scope.status = 'Unable to delete music in album, please refresh and try again. Error message: ' + data.errors;
                }
                $scope.showStatus();
            })
            .error(function (error) {
                $scope.status = 'Unable to delete music in album, please refresh and try again. Error message: ' + error.message;
                $scope.showStatus();
            });
    };

    $scope.delete_music_in_album = function (album, music) {
        if (confirm("Confirm that you want to remove music: " + music.name + " from album: " + album.name + "? Note this is an irreversible operation.")) {
            userFactory.delete_music_in_album(album.id, music.id)
                .success(function (data) {
                    console.log("should be same:");
                    console.log(data.music);
                    console.log(music);
                    if (data.type === 'success') {
                        var musics = album.musics;
                        for (var i = musics.length - 1; i >= 0; i--) {
                            if (musics[i].id === music.id) {
                                musics.splice(i, 1);
                                break;
                            }
                        }

                        // update albumList in home page.
                        allFactory.get_albums_by_sound($scope.currentSound.id)
                            .success(function (data) {
                                $scope.albumList = data;
                            });

                        // update current album's musics
                        if(album.id == $scope.currentAlbum.id){
                            var currentMusics = $scope.currentAlbum.musics;

                            for (var i = currentMusics.length - 1; i >= 0; i--) {
                                if (currentMusics[i].id === music.id) {
                                    currentMusics.splice(i, 1);
                                    b_creak;
                                }
                            }
                        }

                        $scope.status = 'Success delete music' + music.name + ' from album ' + album.name;
                    } else {
                        $scope.status = 'Unable to delete music in album, please refresh and try again. Error message: ' + data.errors;
                    }
                    $scope.showStatus();
                })
                .error(function (error) {
                    $scope.status = 'Unable to delete music in album, please refresh and try again. Error message: ' + error.message;
                    $scope.showStatus();
                });
        }
        console.log(album);
    };

    $scope.delete_unused_sound = function (sound) {
        if (confirm("Confirm that you want to delete this sound: " + sound.name + "? Note this is an irreversible operation.")) {
            userFactory.delete_unused_sound(sound.id)
                .success(function (data) {
                    if (data.type === 'success') {
                        for (var i = $scope.all_sounds.length - 1; i >= 0; i--) {
                            if ($scope.all_sounds[i].id === sound.id) {
                                $scope.all_sounds.splice(i, 1);
                                break;
                            }
                        }
                        for (var i = $scope.user_sounds.length - 1; i >= 0; i--) {
                            if ($scope.user_sounds[i].id === sound.id) {
                                $scope.user_sounds.splice(i, 1);
                                break;
                            }
                        }

                        $scope.updateSelfProfile();
                        
                        $scope.status = 'Success delete sound' + sound.name;
                    } else {
                        $scope.status = 'Unable to delete sound, please refresh and try again. Error message: ' + data.errors;
                    }
                    $scope.showStatus();
                })
                .error(function (error) {
                    $scope.status = 'Unable to delete sound, please refresh and try again. Error message: ' + error.message;
                    $scope.showStatus();
                });
        }
    };

    $scope.delete_unused_music = function (music) {
        if (confirm("Confirm that you want to delete this music: " + music.name + "? Note this is an irreversible operation.")) {
            userFactory.delete_unused_music(music.id)
                .success(function (data) {
                    if (data.type === 'success') {
                        for (var i = $scope.user_musics.length - 1; i >= 0; i--) {
                            if ($scope.user_musics[i].id === music.id) {
                                $scope.user_musics.splice(i, 1);
                                break;
                            }
                        }
                        $scope.status = 'Success delete music' + music.name;
                    } else {
                        $scope.status = 'Unable to delete music, please refresh and try again. Error message: ' + data.errors;
                    }
                    $scope.showStatus();
                })
                .error(function (error) {
                    $scope.status = 'Unable to delete music, please refresh and try again. Error message: ' + error.message;
                    $scope.showStatus();
                });
        }
    };

    $scope.delete_user_album = function (album) {
        if (confirm("Confirm that you want to delete this album: " + album.name + "? Note this is an irreversible operation.")) {
            userFactory.delete_user_album(album.id)
                .success(function (data) {
                    if (data.type === 'success') {
                        console.log(album);

                        for (var i = $scope.user_albums.length - 1; i >= 0; i--) {
                            if ($scope.user_albums[i].id === album.id) {
                                $scope.user_albums.splice(i, 1);
                                break;
                            }
                        }
                        for (var i = $scope.user_favorite_albums.length - 1; i >= 0; i--) {
                            if ($scope.user_favorite_albums[i].id === album.id) {
                                $scope.user_favorite_albums.splice(i, 1);
                                break;
                            }
                        }

                        $scope.updateSelfProfile();

                        $scope.status = 'Success delete album ' + album.name;
                    } else {
                        $scope.status = 'Unable to delete album, please refresh and try again. Error message: ' + data.errors;
                    }
                    $scope.showStatus();
                })
                .error(function (error) {
                    $scope.status = 'Unable to delete album, please refresh and try again. Error message: ' + error.message;
                    $scope.showStatus();
                });
        }
    };

    // check if album in user's favorite list
    $scope.checkFavorite = function (album) {

        if ($scope.user_favorite_albums === undefined || $scope.user_favorite_albums.length == 0) {
            return false;
        }

        var len = $scope.user_favorite_albums.length;
        for (var i = 0; i < len; i++) {
            if ($scope.user_favorite_albums[i].id == album.id)
                return true;
        }
        return false;
    };

    /*** music popover functions***/

    // show add music popover
    $scope.addPopoverVisible = false;
    $scope.showAddtoPopover = function (music) {
        // the selected music to be add in a album
        $scope.selectedMusic = music;

        $scope.addPopoverVisible = true;
        // show animation
        $('#music-popover').css({'display': 'block'});
        $("#music-popover").animate({opacity: 1}, 100);
    };

    /*** music popover functions***/
    $(document).mouseup(function (e) {

        // hide the add music popover when click outside
        if ($scope.addPopoverVisible && !$("#music-popover").is(e.target)
            && $("#music-popover").has(e.target).length === 0) {
            $("#music-popover").animate({opacity: '0'}, 100, function () {
                $('#music-popover').css({'display': 'none'});
                $scope.addPopoverVisible = false;
            });
        }
    });

    // check selectedMusic in which album
    $scope.checkMusicInAlbum = function (album, music) {
        if (music == undefined) return false;
        for (var i = 0; i < album.musics.length; i++) {
            if (album.musics[i].id === music.id) {
                album.selected = true;
                return true;
            }
        }
        album.selected = false;
        return false;
    };

    // add or delete music in album
    $scope.changeMusicInAlbum = function (album, music) {

        if (album.selected) {
            $scope.add_music_in_album(album, music);
        }
        else {
            console.log("delete!");
            $scope.delete_music_in_album(album, music);
        }
        
    };

    // init new album list when create new music
    // set the first album as default;
    $scope.initNewMusicAlbumList = function () {
        if ($scope.user_albums.length == 0) return;

        $scope.user_albums[0].added = true;

        for (var i = 1; i < $scope.user_albums.length; i++) {
            $scope.user_albums[i].added = false;
        }
    };

    function init_all_content() {

        allFactory.get_all_sounds()
            .success(function (data) {
                $scope.all_sounds = data;
                $scope.currentSound = data[0];

                // init current album and music
                if(!$scope.isHome) return;
                allFactory.get_albums_by_sound(data[0].id)
                    .success(function (data) {
                        $scope.albumList = data;
                        $scope.currentAlbum = data[0];
                        $scope.currentMusic = data[0].musics[0];
                        console.log("init all: ",$scope.currentAlbum);
                    })
                    .error(function (error) {
                        $scope.status = 'Unable to load all sounds data, please refresh and try again. Error message: ' + error.message;
                        $scope.showStatus();
                    });

            })
            .error(function (error) {
                $scope.status = 'Unable to load all sounds data, please refresh and try again. Error message: ' + error.message;
                $scope.showStatus();
            });
    }

    function init_user_content() {
        // get logged user
        userFactory.get_user()
            .success(function (data) {
                $scope.currentUser = data.user;

                if ($scope.currentUser == undefined) return;

                $scope.image.imgSrc = '/meditation/get-user-image/' + $scope.currentUser.id;

                userFactory.get_user_albums()
                    .success(function (data) {
                        $scope.user_albums = data;
                    })
                    .error(function (error) {
                        $scope.status = 'Unable to load user albums data, please refresh and try again. Error message: ' + error.message;
                        $scope.showStatus();
                    });

                userFactory.get_user_sounds()
                    .success(function (data) {
                        $scope.user_sounds = data;
                    })
                    .error(function (error) {
                        $scope.status = 'Unable to load user sounds data, please refresh and try again. Error message: ' + error.message;
                        $scope.showStatus();
                    });

                userFactory.get_user_musics()
                    .success(function (data) {
                        $scope.user_musics = data;
                    })
                    .error(function (error) {
                        $scope.status = 'Unable to load user musics data, please refresh and try again. Error message: ' + error.message;
                        $scope.showStatus();
                    });

                userFactory.get_user_favorite_albums()
                    .success(function (data) {
                        $scope.user_favorite_albums = data;
                    })
                    .error(function (error) {
                        $scope.status = 'Unable to load user favorite albums data, please refresh and try again. Error message: ' + error.message;
                        $scope.showStatus();
                    });

            })
            .error(function (data) {
                $scope.status = 'Unable to load currentUser, please refresh and try again. Error message: ' + error.message;
                $scope.showStatus();
            });

    }

    // show status bar
    $scope.showStatus = function(){
        $('#status-bar').attr('class', 'alert alert-warning fade in');
        setTimeout(function () {
            $('#status-bar').attr('class', 'alert alert-warning fade out');
        }, 3000);
    };

    $('body').keydown(function (e) {
        if (e.which == 81) {
            console.log($scope.currentSound);
            console.log($scope.currentAlbum);
            console.log($scope.currentMusic);
            // console.log($scope.albumList);
            console.log($scope.profileAlbums);
            console.log($scope.user_albums);
            console.log($scope.user_favorite_albums);
            // console.log("currentUser: ",$scope.currentUser);
            // console.log($scope.user_favorite_albums);
            // console.log($scope.user_albums);
        }
    });

});