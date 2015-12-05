var app = angular.module('profileControllerModule', []);

app.controller('profileController', function ($scope, $http, Upload, userFactory) {

    $scope.user_id;
    $scope.imgSrc;
    $scope.profile;

    $scope.editProfileError;
    $scope.changePasswordError;


    $scope.save_edit_profile = function () {
        if ($scope.profile_data) {
            if ($scope.profile_data.first_name || $scope.profile_data.last_name || $scope.profile_data.bio || $scope.profile_data.image) {
                Upload.upload({
                    url: '/meditation/edit-user-profile',
                    data: {
                        'first_name': $scope.profile_data.first_name,
                        'last_name': $scope.profile_data.last_name,//$scope.profile.last_name,
                        'bio': $scope.profile_data.bio,//$scope.profile.bio,
                        'image': $scope.profile_data.image//$scope.profile.image
                    }
                }).success(function (data) {
                    if (data.type == 'success') {

                        $scope.profile = data.profile;

                        // force image to reload
                        $scope.image.imgSrc = '/meditation/get-user-image/' + $scope.user_id + '?' + new Date().getTime();
                        //$scope.status = 'Success editing profile.';
                        $scope.editProfileError = 'Success editing profile.';
                        setTimeout(function () {
                            $('#change-profile-popup').modal('hide');
                            $scope.editProfileError = '';
                        }, 1000);
                    } else {
                        //$scope.status = data.errors;
                        $scope.editProfileError = data.errors.join(' And ');
                    }
                }).error(function (error) {
                    $scope.status = 'Unable to save edit profile, please refresh and try again. Error message: ' + error.message;
                    $scope.editProfileError = 'Unable to save edit profile, please refresh and try again. Error message: ' + error.message;
                });
            }
        } else {
            $scope.editProfileError = 'Please fill something to change profile.';
        }
    };

    $scope.changePassword = function () {
        if ($scope.oldPassword && $scope.newPassword1 && $scope.newPassword2) {
            $http.post('/meditation/change-password-inner', {
                'old_password': $scope.oldPassword,
                'new_password1': $scope.newPassword1,
                'new_password2': $scope.newPassword2
            })
                .success(function (data) {
                    if (data.type == 'success') {
                        $('#change_password_form_inner').get(0).reset();
                        //$scope.status = 'success changing password.';
                        $scope.changePasswordError = 'success changing password.';
                        setTimeout(function () {
                            $('#change-password-popup').modal('hide');
                            $scope.changePasswordError = '';
                        }, 1000);

                    } else {
                        //$scope.status = data.errors;
                        $scope.changePasswordError = data.errors.join(' And ');
                    }
                })
                .error(function (error) {
                    $scope.status = 'fail to change password, please refresh and try again.';
                });
        } else {
            $scope.changePasswordError = 'Please fill all fields to change password.';
        }
    };
    init_user_profile();

    function init_user_profile() {
        $scope.setIsHome(false);
        $scope.user_id = window.location.href.substr(window.location.href.lastIndexOf('/') + 1);
        if ($scope.user_id && !isNaN($scope.user_id)) {
            $scope.imgSrc = '/meditation/get-user-image/' + $scope.user_id;
            
            if($scope.user_id == "#" || !$scope.user_id) return;

            get_current_profile();

            // set user profile's albums:
            userFactory.get_other_albums($scope.user_id)
                .success(function (data) {
                    // $scope.user_albums = data;
                    // $scope.currentAlbum = data[0];

                    $scope.setProfileAlbums(data);

                    $scope.setCurrentAlbum({});
                    $scope.setCurrentSound({});
                    $scope.setCurrentMusic({});

                })
                .error(function (error) {
                    $scope.status = 'Unable to load user albums data, please refresh and try again. Error message: ' + error.message;
                });

            // set user profile's sound:
            userFactory.get_other_sounds($scope.user_id)
                .success(function (data) {
                    // $scope.user_sounds = data;
                    // $scope.currentSound = data[0];

                    $scope.setProfileSounds(data);
                })
                .error(function (error) {
                    $scope.status = 'Unable to load user sound data, please refresh and try again. Error message: ' + error.message;
                });

            // set user profile's favorite albums
            userFactory.get_other_favorite_albums($scope.user_id)
                .success(function (data) {
                    // $scope.user_favorite_albums = data;
                    $scope.setProfileFavorites(data);
                })
                .error(function (error) {
                    $scope.status = 'Unable to load user favorite albums data, please refresh and try again. Error message: ' + error.message;
                });
        }
    }

    function get_current_profile() {
        $http.get('/meditation/get-user-profile/' + $scope.user_id)
            .success(function (data) {
                $scope.setOtherUser(data.profile.user);

                if (data.type == 'success') {
                    $scope.profile = data.profile;
                } else {
                    $scope.status = 'Unable to init_user_profile, please refresh and try again. Error message: ' + data.errors;
                }
            })
            .error(function (error) {
                $scope.status = 'Unable to init user profile, please refresh and try again. Error message: ' + error.message;
            });
    }

});