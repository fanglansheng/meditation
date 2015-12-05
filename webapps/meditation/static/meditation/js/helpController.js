var app = angular.module('helpControllerModule', []);

app.controller('helpController', function ($scope) {
    $scope.faqs = [
        {
            id: 1,
            question: 'What is and How to use this website?',
            answer: 'This website provides users with a mix of nature sounds (white noise as environment) and music to help them relax and meditate. ' +
            'You can share, upload, favorite, use other users albums, sounds and musics.'
        },
        {
            id: 2,
            question: 'Is it tedious to copy and paste urls every time I create music and sound?',
            answer: 'Yes. We have extensions/plugins for you to pin media. ' +
            'You can click the button to download extension and install to use. ' +
            'Currently chrome extension is available. And this extension is only used for youtube video linking. ' +
            'You should upload the extension folder through chrome extension center, by clinking developer mode.'
        },
        {
            id: 3,
            question: 'What is the structure of this website?',
            answer: 'We have many natural sounds as environments that you can use to create your albums, and put musics into them. ' +
            'You are free to upload your video taped sound or just provide a youtube link, then we know your sound. ' +
            'You can also pin music from youtube to your albums.'
        },
        {
            id: 4,
            question: 'I cannot view the videos nor listen to musics.',
            answer: 'It might be because your current location does not support youtube, which is our main video source. ' +
            'Or maybe the media provided is not valid.'
        },
        {
            id: 5,
            question: 'Can I upload my own music? Is it authorized to upload?',
            answer: 'You cannot upload commercial musics to this website. Instead, ' +
            'you will need our plugins or copy and paste youtube urls to link your favorite music. ' +
            'And you can upload your favorite natural sounds which is recorded by you, and share them to all users to make albums.'
        },
        {
            id: 6,
            question: 'What is an environment?',
            answer: 'An environment is a natural sound (white noise) that you can create by uploading your recordings, ' +
            'or pin it from youtube with provided url and our extension. ' +
            'You can use one environment to create an album. By setting an environment, you can see all albums for that environment.'
        },
        {
            id: 7,
            question: 'How can I pin the music?',
            answer: 'We have provided you an extension to pin music from youtube with chrome. You can also copy and paste the video url. ' +
            'Pin music by providing several albums can add the music to your albums.'
        },
        {
            id: 8,
            question: 'How can I create an album?',
            answer: 'You can create your album anywhere in our site by assigning an environment to that album. ' +
            'You can see albums by environments.'
        },
        {
            id: 9,
            question: 'Can I upload my music?',
            answer: 'We do not allow users uploading musics, which violates song copyrights. ' +
            'Instead, users can pin music from media site like youtube.'
        },
        {
            id: 10,
            question: 'About this site?',
            answer: 'All rights reserved. You can email us with all your concern to meditation.noreply@gmail.com.'
        }
    ];

    $scope.download = function () {
        document.getElementById('download-frame').src = '/static/meditation/res/meditation-extension.zip';
    };

});