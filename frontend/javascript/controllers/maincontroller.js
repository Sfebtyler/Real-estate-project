var app = angular.module('realestate');

app.controller('MainController', function(user, home, $window, $scope, $location, $routeParams, $http, $timeout, $route) {

    var vm = this;
    vm.user = user;
    vm.home = home;
    vm.username = '';
    vm.password = '';
    vm.homeslist = [];
    vm.premiumhomeslist = [];
    vm.homespagelist = [];
    vm.premiumhomepagelist = [];
    vm.favoritespagelist = [];
    vm.there_is_premium_house = false;
    vm.there_is_house = false;
    vm.search_input = '';
    vm.startmessage = false;
    vm.guestname = '';
    vm.guestphone = '';
    vm.guestemail = '';
    vm.message = '';
    vm.botsecurity = false;
    vm.opensearch = false;
    vm.opendetailspage = false;
    vm.detailhouseid = '';
    vm.login_clicked = false;

    vm.scroll = function() {

            var currpath = $location.path();
            if (currpath == '/homespage' && vm.homeslist.response.next) {
                var homesnext = vm.homeslist.response.next;
                console.log(homesnext);
                $http.get(homesnext)
                .then(function(response) {
                    if(vm.homespagelist.indexOf(homesnext) == -1){
                        vm.homespagelist.push(homesnext);
                        vm.homeslist.results = vm.homeslist.results.concat(response.data.results);
                        vm.homeslist.response = response.data;
                    }
                },
                    function(err) {
                        console.log(err);
                    });
            }
            if (currpath == '/home' && vm.premiumhomeslist.response !== undefined && vm.premiumhomeslist.response.next) {
                var premiumsnext = vm.premiumhomeslist.response.next;
                $http.get(premiumsnext)
                .then(function(response) {
                    if (vm.premiumhomepagelist.indexOf(premiumsnext) == -1) {
                        vm.premiumhomepagelist.push(premiumsnext);
                        vm.premiumhomeslist.results = vm.premiumhomeslist.results.concat(response.data.results);
                        vm.premiumhomeslist.response = response.data;
                    }
                },
                    function(err) {
                        console.log(err);
                    });
            }
            if (currpath == '/favorites' && vm.favoriteslist.response.next) {
                var favoritesnext = vm.favoriteslist.response.next;
                console.log(favoritesnext);
                $http.get(favoritesnext)
                .then(function(response) {
                    if (vm.favoritespagelist.indexOf(favoritesnext) == -1) {
                        vm.favoritespagelist.push(favoritesnext);
                        vm.favoriteslist.results = vm.favoriteslist.results.concat(response.data.results);
                        vm.favoriteslist.response = response.data;
                    }
                });
            }
    };

    vm.sendmessage = function () {
        var linebreak = String.fromCharCode(13);
        if (vm.botsecurity === true) {
            console.log(vm.message);
            $http.post('http://127.0.0.1:8000/contact-us/', {
                name: vm.guestname,
                subject: 'Homes lead',
                email: 'sfebtyler@yahoo.com',
                text: vm.message + linebreak +
                linebreak +
                linebreak +
                'Contact info:' + linebreak +
                'Phone Number:' + vm.guestphone + linebreak +
                'Email:' + vm.guestemail,
            }).then(function () {
                vm.startmessage = false;
            });
        } else {
            console.log('you are not human');
            vm.startmessage = true;
        }
    };


    vm.getContactInfoOnPageLoad = function () {
            user.getContactInfo()
            .then(function (response) {
                vm.listed_agent_name = response.listed_agent_name;
                vm.listed_phone_number = response.listed_phone_number;
                vm.listed_email = response.listed_email;
            });
    };


    // will need to be on the main controller
    vm.reroute = function (endofpath, id) {
        if (id) {
            $location.path(endofpath + id);
        } else {
            $location.path(endofpath);
        }

        if ($location.path() == '/homespage') {
            vm.getHomesList();
        }
    };

    // will need to be on the main controller
    vm.search = function () {
        if(vm.search_input.length === 0) {
            vm.getHomesList();
        }
        if(vm.search_input.length > 3) {
            $location.path('/homespage');
            vm.homeslist = [];
            $http.get('http://127.0.0.1:8000/homes/', {
                params: {q: vm.search_input}
        })
        .then(function (response) {
            console.log(response.data);
            vm.homeslist = {'response':response.data, 'results': response.data.results};
        });
        }
        vm.opensearch = false;
    };

    vm.pageloadhomedetails = function () {
        //this function just grabs the data on page load rather than relying on the reroute function

        vm.home.getlistingdetail(vm.detailhouseid).then(function(response) {
            vm.listingdetail = response;
            console.log(response);
        })
        .then(function() {
            vm.home.getlistingdetail(vm.detailhouseid + '/' + 'extra_images').then(function(response) {
                vm.listingdetail.extraimages = response;
            });
        });
    };

    // will need to be on the main controller
    vm.isAuthenticated = function () {
        if ($window.localStorage.getItem('Token')) {
            var token = $window.localStorage.getItem('Token');
            if (token) {
                vm.getCurrentUser();
                vm.current_user = true;
                vm.login_clicked = true;
                return;
            } else {
                vm.current_user = false;
                vm.login_clicked = false;
                return;
            }
        }
    };

    vm.getCurrentUser = function () {
        vm.user.getCurrentUser()
        .then(function (data) {
            vm.current_user = data;
            vm.current_user.id = data.id;
        });
    };

    // will need to be on the main controller
    vm.login = function () {
        vm.user.login(vm.username, vm.password)
        .then(function () {
            vm.getCurrentUser();
            $route.reload();
        });
    };

    // will need to be on the main controller
    vm.logout = function () {
            vm.user.logout();
            vm.current_user = false;
            vm.login_clicked = false;
            if ($location.path() == '/favorites') {
                vm.reroute('/home');
            }
    };

    // will need to be on the main controller
    vm.getHomesList = function () {
        vm.homespagelist = [];

        vm.home.getHomeListings().then(function (response) {
            vm.homeslist = {'response':response, 'results': response.results};
        });
    };


    vm.getPremiumHomesList = function () {
        vm.premiumhomepagelist = [];

        vm.home.getPremiumListings().then(function (response) {
            vm.premiumhomeslist = {'response':response, 'results': response.results};
        });
    };

    // will need to be on the main controller
    vm.favorite = function (id, currentuser) {
        vm.home.addToFavorites(id, currentuser);
    };

    vm.getFavorites = function () {
        if (vm.current_user === false) {
            vm.reroute('/home');
        } else {
            vm.favoriteslist = [];
            vm.home.getFavorites()
            .then(function(response) {
                vm.favoriteslist.results = vm.favoriteslist.concat(response.results);
                vm.favoriteslist.response = response;
            });
        }
    };

    vm.deleteFromFavorites = function (homeid, userid) {
        vm.home.deleteFavorite(homeid, userid)
        .then(function () {
            if ($location.path() == '/favorites')
                $timeout(function () {
                    vm.favoriteslist.results.forEach(function (home, index) {
                    if (home.id == homeid) {
                        vm.favoriteslist.results.splice(index, 1);
                    }
                }, 100);
            });
        });
    };

});
