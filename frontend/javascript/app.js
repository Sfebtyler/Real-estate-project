(function() {
var app = angular.module('realestate', ['vcRecaptcha', 'routes', 'infinite-scroll', 'ngMaterial']);


app.factory('authInterceptor', function($location, $q, $window) {

    return {
    'request': function(config) {
        var token = $window.localStorage.getItem('Token');

        config.headers = config.headers || {};
        if (token) {
            config.headers.Authorization = 'Token ' + token;
        }
        return config;
        }
    };
})

.config(function($httpProvider) {
    $httpProvider.interceptors.push('authInterceptor');
});

})();
