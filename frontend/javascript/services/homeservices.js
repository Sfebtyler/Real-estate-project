var app = angular.module('realestate');

app.service('home', function ($http, $q, $window, $routeParams) {
    var that = this;

    that.getHomeListings = function () {
        return $http.get('http://127.0.0.1:8000/homes/?all=true')
        .then(function (response) {
            console.log('success', response.data);
            response.data.results.forEach(function(house) {
                house.price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
            });
            return response.data;
        });
    };

    that.getPremiumListings = function () {
        return $http.get('http://127.0.0.1:8000/homes/?premium_homes=true')
        .then(function (response) {
            console.log(response);
            response.data.results.forEach(function(house) {
                house.price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
            });
            return response.data;
        });
    };

    that.getlistingdetail = function (id, fullurl) {
        if (!fullurl) {
            return $http.get('http://127.0.0.1:8000/homes/' + id + '/')
            .then(function(response) {

                return response.data;
            });
        } else {
            return $http.get(fullurl)
            .then(function(response) {
                console.log(response);
                return response.data;
            });
        }
    };

    that.addToFavorites = function (homeid, userid) {
        return $http.post('http://127.0.0.1:8000/favorites/', {
            list: homeid,
            user: userid
        })
        .then(function(response) {
            console.log(response);
            return response.data;
        });
    };

    that.deleteFavorite = function (homeid, userid) {
        return $http.post('http://127.0.0.1:8000/homes/delete_favorite/', {
            list: [homeid],
            user: userid.id
        });
    };

    that.getFavorites = function () {
        return $http.get('http://127.0.0.1:8000/homes/?favorites=true')
        .then(function(response) {
            response.data.results.forEach(function(house) {
                house.price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
            });
            return response.data;
        });
    };

});
