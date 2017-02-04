(function() {
var app = angular.module('realestate', ['vcRecaptcha', 'routes', 'infinite-scroll', 'ngMaterial']);


app.directive("scroll", function ($window, $document) {
    return function(scope, element, attrs) {
        var last_known_scroll_position = 0;
        var ticking = false;
        angular.element(document).on("scroll", function() {
            infinite_scroll = function(scrollpos) {
                console.log(scrollpos);
                if (scrollpos >= $window.scrollHeight - 50) {
                    console.log('load more');
                }
            };

            // I am having trouble with the Yoffset not updating
              last_known_scroll_position = $window.scrollY;
              if (!ticking) {
                $window.requestAnimationFrame(function() {
                  infinite_scroll(last_known_scroll_position);
                  ticking = false;
                });
              }
              ticking = true;
            scope.$apply();
        });
    };
});


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
