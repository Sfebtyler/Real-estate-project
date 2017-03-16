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

    this.createlogin = function (cusername, cemail, cpassword, cphone) {
        return $http.post('http://127.0.0.1:8000/users/', {
            username: cusername,
            email: cemail,
            password: cpassword,
            phone_number: cphone
        })
        .then(function(response) {
            $http.post('http://127.0.0.1:8000/users/create_profile/', {
                user: response.data.id,
                phone_number: cphone
            }).then(function(response){
                console.log("profile", response);
            });

            console.log(response);
        });
    };

    this.checkifuniqueuser = function(cusername) {
        return $http.get('http://127.0.0.1:8000/users/check_if_exists/', {
                params: {q: cusername}
        });
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
