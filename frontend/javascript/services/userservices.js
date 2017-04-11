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

    this.createlogin = function (cusername, cfirstname, clastname, cemail, cpassword, cphone) {
        return $http.post('http://127.0.0.1:8000/users/', {
            username: cusername,
            first_name: cfirstname,
            last_name: clastname,
            email: cemail,
            password: cpassword,
            phone: cphone,
        })
        .then(function(response) {
            console.log(response);
        });
    };

    this.updateprofile = function (first_name, last_name, email, phone, id) {
        postDocument = {};

        if (first_name !== '' && first_name !== undefined) {
            postDocument.first_name = first_name;
        }

        if (last_name !== '' && last_name !== undefined) {
            postDocument.last_name = last_name;
        }

        if (email !== '' && email !== undefined) {
            postDocument.email = email;
        }

        if (phone !== '' && phone !== undefined) {
            postDocument.phone = phone;
        }

        return $http.patch('http://127.0.0.1:8000/users/' + id + '/', postDocument)
        .then(function (response) {
            console.log(response);
        });
    };

    this.sendpasswordresetrequest = function (send_to_email) {
        return $http.post('http://127.0.0.1:8000/password-reset/', {
            to_email: send_to_email,
        })
        .then(function(response) {
            console.log(response);
        });
    };

    this.updatePassword = function (token, newpassword) {
        return $http.post('http://127.0.0.1:8000/password-reset/confirm_reset/', {
            temptoken: token,
            password: newpassword
        }).then(function(response) {
            console.log(response);
            return response.data;
        });
    };

    this.checkifuniqueuser = function(cusername) {
        return $http.get('http://127.0.0.1:8000/users/check_if_user_exists/', {
                params: {q: cusername}
        });
    };

    this.checkifuniqueemail = function(cemail) {
        return $http.get('http://127.0.0.1:8000/users/check_if_email_exists/', {
                params: {q: cemail}
        });
    };

    this.getCurrentUser = function () {
        return $http.get('http://127.0.0.1:8000/users/current_user/')
        .then(function (response) {
            that.profiledetails = response;
            return response.data;
        });
    };

    this.getContactInfo = function () {
        return $http.get('http://127.0.0.1:8000/contacts/')
        .then(function (response) {
            console.log(response.data.results[0]);
            return response.data.results[0];
        });
    };

});
