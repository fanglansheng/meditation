var app = angular.module('albumControllerModule', []);

app.controller('albumController', function ($scope, $http, $sce, allFactory, userFactory) {

    $scope.isProfile = false;
    $scope.firstSetEnviron = true;
    // init sidebar's show attribute:
    $scope.albumSidebarVisible = false;

    // the music selected to add in album
    $scope.selectedMusic;

    $scope.pauseIcon = "glyphicon glyphicon-pause";
    $scope.ctrlBtnIcon = "glyphicon glyphicon-triangle-top";

    init();

    function init(){
        console.log("init albumController");
        // show set environment modal
        $('#environment-popup').modal('show');
        $('#launch-btn').prop("disabled",true);

        // video from youtube
        loadYoutubePlayer();
    }

    // click event callback: show or hide the bottom sidebar
    $scope.showSidebar = function(){

        $scope.albumSidebarVisible = !$scope.albumSidebarVisible;

        if($scope.albumSidebarVisible){
            $("#album-sidebar").animate({bottom: '0px'});
            $scope.ctrlBtnIcon = "glyphicon glyphicon-triangle-bottom";
        }
        else{
            $("#album-sidebar").animate({bottom: '-240px'});
            $scope.ctrlBtnIcon = "glyphicon glyphicon-triangle-top";
        }
    };

    // play selected music
    $scope.playMusic = function(music){

        $scope.soundMuteIcon = "glyphicon glyphicon-volume-off";
        $scope.pauseIcon = "glyphicon glyphicon-pause";
        // store selected album index
        $scope.setCurrentMusic(music);

        // play selected music
        $scope.musicPlayer.loadVideoById(getVideoId(music.url));
    };

    // play selected album
    $scope.playAlbum = function(album){

        // store selected album index
        $scope.setCurrentAlbum(album);

        if(album.musics.length == 0){
            $scope.setCurrentMusic(null);
            $scope.musicPlayer.loadVideoById("");
            return;
        }

        // play the first music in this album
        $scope.setCurrentMusic(album.musics[0]);
        $scope.playMusic(album.musics[0]);

    };

    $scope.playAlbumWithSound = function(album){

        $scope.playAlbum(album);

        $scope.setCurrentAlbum(album);
        $scope.setCurrentSound(album.sound);

        if(album.sound.url){
            $("#user-video").parent().get(0).pause();

            // play selected sound video
            $scope.videoPlayer.loadPlaylist([getVideoId(album.sound.url)],0,3);
            $scope.videoPlayer.setLoop(true);

        }
        else if(album.sound.content){
            // console.log(src);
            $scope.videoPlayer.pauseVideo();
            $("#user-video").attr("src", "/meditation/get-sound-content/" + album.sound.id);
            $("#user-video").parent().attr("poster", "/meditation/get-sound-image/" + album.sound.id);
            $("#user-video").parent().get(0).load();
        }

    };


    // play sound and show the album list
    $scope.playSound = function(sound){

        $scope.firstSetEnviron = false;
        $scope.pauseIcon = "glyphicon glyphicon-pause";

        if(sound.url){
            $("#user-video").parent().get(0).pause();

            // play selected sound video
            // $scope.videoPlayer.loadVideoById(getVideoId(sound.url));
            $scope.videoPlayer.loadPlaylist([getVideoId(sound.url)],0,3);
            $scope.videoPlayer.setLoop(true);
            // $scope.videoPlayer.loadVideoByUrl('http://www.youtube.com/v/MOdBhbpMoz4?version=3');

            // get albums list whose sound field is selected sound
            allFactory.get_albums_by_sound(sound.id)
                .success(function (data){

                    $scope.setAlbumList(data);
                    // set the first album as default album
                    $scope.setCurrentAlbum(data[0]);

                    // init musics
                    $scope.setCurrentMusic(null);

                    $scope.musicPlayer.loadVideoById("");
                });
        }
        else if(sound.content){
             //var src = allFactory.get_sound_content(sound.id);
            // console.log(src);
            $scope.videoPlayer.pauseVideo();
            $("#user-video").attr("src", "/meditation/get-sound-content/" + sound.id);
            $("#user-video").parent().attr("poster", "/meditation/get-sound-image/" + sound.id);
            $("#user-video").parent().get(0).load();
            allFactory.get_albums_by_sound(sound.id)
                .success(function (data){
                    $scope.setAlbumList(data);
                    // set the first album as default album
                    $scope.setCurrentAlbum(data[0]);
                });
        }

    };

    // play next music in album
    $scope.playNextMusic = function(){
        var musicList = $scope.getCurrentAlbum().musics;

        if(!musicList) return;
        // set current music
        for(var i=0; i < musicList.length; i++){
            if($scope.currentMusic === musicList[i]){
                var nextMusicIndex = (i+1) % musicList.length;
                $scope.setCurrentMusic(musicList[nextMusicIndex]);
                break;
            }
        }
        $scope.musicPlayerId = $scope.currentMusic.url;
        $scope.musicPlayer.loadVideoById(getVideoId($scope.musicPlayerId));
    };

    // play or pause current music
    $scope.pauseMusic = function(){
        // get current status
        var status = $scope.musicPlayer.getPlayerState();

        // console.log(status);
        if(status == YT.PlayerState.PLAYING){
            $scope.musicPlayer.pauseVideo();
            $scope.pauseIcon = "glyphicon glyphicon-play";
        }
        else if(status == YT.PlayerState.PAUSED){
            $scope.musicPlayer.playVideo();
            $scope.pauseIcon = "glyphicon glyphicon-pause";
        }
    };

    $scope.soundMuteIcon = "glyphicon glyphicon-volume-off";
    $scope.pauseSound = function(){
        // get current status
        var status = $scope.videoPlayer.getPlayerState();

        // console.log(status);
        if(status == YT.PlayerState.PLAYING){
            $scope.videoPlayer.pauseVideo();
            $scope.soundMuteIcon = "glyphicon glyphicon-volume-up";
        }
        else if(status == YT.PlayerState.PAUSED){
            $scope.videoPlayer.playVideo();
            $scope.soundMuteIcon = "glyphicon glyphicon-volume-off";
        }
    };

    /*************************************/
    /** video functions **/
    function loadYoutubePlayer() {
        // This code loads the IFrame Player API code asynchronously.
        if (typeof(YT) == 'undefined' || typeof(YT.Player) == 'undefined') {
            var tag = document.createElement('script');
            tag.src = "https://www.youtube.com/iframe_api";
            var firstScriptTag = document.getElementsByTagName('script')[0];
            firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

            window.onYouTubePlayerAPIReady = function() {
                createYouTubeVideo();
            };
        }
        else {
            createYouTubeVideo();
        }
    }

    // This function creates an <iframe> (and YouTube player)
    // after the API code downloads.
    function createYouTubeVideo() {
        //console.log($scope.isProfile);
        if($scope.isProfile){
            $scope.videoPlayer = new YT.Player('youtube-video', {
                height: '10',
                width: '0',
                videoId: "",
                events: {
                    'listType':'playlist',
                    'loop': 1 ,
                    'onReady': onPlayerReady,
                    'onStateChange': onPlayerStateChange
                }
            });
        }
        else{
            $scope.videoPlayer = new YT.Player('youtube-video', {
                height: '600',
                width: '100%',
                videoId: '',//getVideoId($scope.soundList[0].url),
                playerVars: {
                    'listType':'playlist',
                    'loop': 1 ,
                    'autoplay': 1,
                    'controls': 0,
                    'showinfo': 0,
                    'autohide': 1,
                    'rel' : 0
                },
                events: {
                    'onReady': onPlayerReady
                    // 'onStateChange': onPlayerStateChange
                }
            });
        }

        $scope.musicPlayer = new YT.Player('music-video', {
            height: '10',
            width: '0',
            videoId: "",
            events: {
                'onReady': onPlayerReady,
                'onStateChange': onPlayerStateChange
            }
        });

        $('#youtube-video').load(function(){
            $('#launch-btn').prop("disabled",false);
        });
    }

    // The API will call this function when the video player is ready.
    function onPlayerReady(event) {
        event.target.playVideo();
    }

    function onPlayerStateChange(event) {
        // play next sound in album when ended
        if (event.data == YT.PlayerState.ENDED) {
            $scope.playNextMusic();
        }
    }

    function getVideoId(url){
        var video_id = url.split('v=')[1];
        console.log("video id:", video_id);
        if(!video_id) return "";

        var ampersandPosition = video_id.indexOf('&');
        if(ampersandPosition != -1) {
          video_id = video_id.substring(0, ampersandPosition);
        }

        return video_id;
    }

});