var app = angular.module('realestate');

app.service('user', function ($http, $q, $window) {
    var that = this;

    this.login = function (tusername, tpassword) {
        var token = $window.localStorage.getItem('Token');
        if (!token) {
            return $http.post('http://127.0.0.1:8000/api-token-auth/', {
                username: tusername,
                password: tpassword
            })
            .then(function (response) {
                $window.localStorage.setItem('Token', response.data.token);
            });
        } else {
            var deferred = $q.defer();
            deferred.resolve();
            return deferred.promise;
        }
    };

    this.logout = function () {
            $window.localStorage.removeItem('Token');
    };

    this.getCurrentUser = function () {
        return $http.get('http://127.0.0.1:8000/users/current_user/')
        .then(function (response) {
            return response.data;
        });
    };

    this.getContactInfo = function () {
        return $http.get('http://127.0.0.1:8000/contacts/')
        .then(function (response) {
            return response.data.results[0];
        });
    };

});
