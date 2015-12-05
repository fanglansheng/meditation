var app = angular.module('authControllerModule', []);

app.controller('authController', function ($scope, $http) {
    $scope.loginError;
    $scope.registerError;
    $scope.resetPasswordError;

    $scope.login = function () {
        $('#registerForm').get(0).reset();
        $scope.registerError = '';
        $('#resetPasswordForm').get(0).reset();
        $scope.resetPasswordError = '';

        if ($scope.login_username && $scope.login_password) {
            $http.post('/meditation/login-auth', {
                'username': $scope.login_username,
                'password': $scope.login_password
            }).success(function (data) {
                if (data.type == 'error') {
                    $scope.loginError = data.errors;

                } else {
                    $scope.loginError = data.content;
                    $('#loginForm').submit();
                }
            })
                .error(function (error) {
                    $scope.loginError = 'Unable to login: ' + error.message;
                });
        } else {
            $scope.loginError = 'Please fill in all login fields.'
        }
    };

    $scope.register = function () {
        $('#loginForm').get(0).reset();
        $scope.loginError = '';
        $('#resetPasswordForm').get(0).reset();
        $scope.resetPasswordError = '';

        if ($scope.register_username && $scope.register_email && $scope.register_password1 && $scope.register_password2) {
            $http.post('/meditation/register', {
                'username': $scope.register_username,
                'email': $scope.register_email,
                'password1': $scope.register_password1,
                'password2': $scope.register_password2
            }).success(function (data) {
                if (data.type == 'error') {
                    $scope.registerError = data.errors.join(" And ");
                } else {
                    $scope.registerError = "Success register";
                    window.location.href = "/meditation/register-info/" + data.username;
                }
            })
                .error(function (error) {
                    $scope.registerError = 'Unable to register: ' + error.message;
                });
        } else {
            $scope.registerError = 'Please fill in all register fields.'
        }
    };

    $scope.reset_password = function () {
        $('#loginForm').get(0).reset();
        $scope.loginError = '';
        $('#registerForm').get(0).reset();
        $scope.registerError = '';

        if ($scope.reset_password_data) {
            if ($scope.reset_password_data.username && $scope.reset_password_data.new_password1 && $scope.reset_password_data.new_password2) {
                $http.post('/meditation/reset-password-email', {
                    'username': $scope.reset_password_data.username,
                    'new_password1': $scope.reset_password_data.new_password1,
                    'new_password2': $scope.reset_password_data.new_password2
                }).success(function (data) {
                    if (data.type == 'error') {
                        $scope.resetPasswordError = data.errors.join(" And ");
                    } else {
                        $scope.resetPasswordError = "Success reset password";
                        window.location.href = "/meditation/reset-password-info/" + data.username;
                    }
                })
                    .error(function (error) {
                        $scope.resetPasswordError = 'Unable to reset password: ' + error.message;
                    });
            } else {
                $scope.resetPasswordError = 'Please fill in all reset password fields.'
            }
        }
    };
    $scope.backToLogin = function () {
        $('#email-reset-password-popup').modal('hide');
        $('#loginForm').get(0).reset();
        $scope.loginError = '';
        $('#registerForm').get(0).reset();
        $scope.registerError = '';
        $('#resetPasswordForm').get(0).reset();
        $scope.resetPasswordError = '';
    };

});