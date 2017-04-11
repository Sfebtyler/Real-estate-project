angular.module('routes',['ngRoute'])
.config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider){
    $routeProvider

    .when('/home', {
    templateUrl: 'templates/pages/home/index.html'
    })
    .when('/homespage', {
        templateUrl: 'templates/pages/home/homespage.html'
    })
    .when('/contacts', {
        templateUrl: 'templates/pages/contacts/index.html'
    })
    .when('/favorites', {
        templateUrl: 'templates/pages/favorites/favorites.html'
    })
    .when('/createlogin', {
        templateUrl: 'templates/pages/logincreate/create.html'
    })
    .when('/search', {
        templateUrl: 'templates/pages/searchpage/searchpage.html'
    })
    .when('/passwordresetrequest', {
        templateUrl: 'templates/pages/logincreate/passwordresetrequest.html'
    })
    .when('/passwordreset/:id', {
        templateUrl: 'templates/pages/logincreate/passwordreset.html'
    })
    .when('/profile', {
        templateUrl: 'templates/pages/logincreate/profile.html'
    })
    .when('/', {
    redirectTo: '/home'
    });

    $locationProvider.html5Mode(true);
}]);
