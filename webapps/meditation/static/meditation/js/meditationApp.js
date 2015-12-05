/*************
MainController has all basic data, other controller will inherate it and override
part of specified data.

*************/

var app = angular.module('meditationApp', ['factoriesModule', 'mainControllerModule',
    'createControllerModule', 'authControllerModule', 'profileControllerModule',
    'helpControllerModule', 'albumControllerModule', 'ngFileUpload', 'ng.django.forms']);

var itemWidth = 170;

// Solve the conflict of django and angularjs
app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});

// Add csrf to angular
app.config(function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});
