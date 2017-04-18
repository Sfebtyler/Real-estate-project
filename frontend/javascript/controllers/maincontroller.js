var app = angular.module('realestate');

app.controller('MainController', function(user, home, $window, $scope, $location, $routeParams, $http, $timeout, $route, $document) {

    var vm = this;
    vm.user = user;
    vm.home = home;
    vm.username = '';
    vm.password = '';
    vm.createusername = '';
    vm.createemail = '';
    vm.createpassword = '';
    vm.createconfirmpassword = '';
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
    vm.existingsearchparams = false;
    vm.passwordresetsendtoemail = '';


    vm.scroll = function() {

            var currpath = $location.path();
            if (currpath == '/homespage' && vm.homeslist.response !== undefined && vm.homeslist.response.next) {
                var homesnext = vm.homeslist.response.next;
                console.log(homesnext);
                $http.get(homesnext)
                .then(function(response) {
                    if(vm.homespagelist.indexOf(homesnext) == -1){
                        response.data.results.forEach(function (house) {
                            house.price = house.price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                        });
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
                        response.data.results.forEach(function (house) {
                            house.price = house.price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                        });
                        vm.premiumhomepagelist.push(premiumsnext);
                        vm.premiumhomeslist.results = vm.premiumhomeslist.results.concat(response.data.results);
                        vm.premiumhomeslist.response = response.data;
                    }
                },
                    function(err) {
                        console.log(err);
                    });
            }
            if (currpath == '/favorites' && vm.favoriteslist.response !== undefined && vm.favoriteslist.response.next) {
                var favoritesnext = vm.favoriteslist.response.next;
                console.log(favoritesnext);
                $http.get(favoritesnext)
                .then(function(response) {
                    if (vm.favoritespagelist.indexOf(favoritesnext) == -1) {
                        response.data.results.forEach(function (house) {
                            house.price = house.price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                        });
                        vm.favoritespagelist.push(favoritesnext);
                        vm.favoriteslist.results = vm.favoriteslist.results.concat(response.data.results);
                        vm.favoriteslist.response = response.data;
                    }
                });
            }
            if (currpath == '/search' && vm.homeslist.response !== undefined && vm.homeslist.response.next) {
                var homesnext = vm.homeslist.response.next;
                console.log(homesnext);
                $http.get(homesnext)
                .then(function(response) {
                    if(vm.homespagelist.indexOf(homesnext) == -1){
                        response.data.results.forEach(function (house) {
                            house.price = house.price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                        });
                        vm.homespagelist.push(homesnext);
                        vm.homeslist.results = vm.homeslist.results.concat(response.data.results);
                        vm.homeslist.response = response.data;
                    }
                },
                    function(err) {
                        console.log(err);
                    });
            }
    };

    vm.scrollToBottom = function () {
            window.scrollTo(0,document.body.scrollHeight);
    };

    vm.setemailparams = function () {
        if (vm.current_user) {
            vm.guestname = vm.current_user.username;
            vm.guestemail = vm.current_user.email;
            vm.guestphone = vm.current_user.phone;
        }
    };

    vm.sendmessage = function () {
        var linebreak = String.fromCharCode(13);
        // if (vm.botsecurity === true) {
            console.log(vm.message);
            $http.post('http://127.0.0.1:8000/contact-us/', {
                name: vm.guestname,
                subject: 'Homes lead',
                email: vm.guestemail,
                text: vm.message + linebreak +
                linebreak +
                linebreak +
                'Contact info: ' + linebreak +
                'Phone Number: ' + vm.guestphone + linebreak +
                'Email: ' + vm.guestemail,
            }).then(function () {
                vm.startmessage = false;
            });
        // } else {
        //     console.log('you are not human');
        //     vm.startmessage = true;
        // }
    };


    vm.getContactInfoOnPageLoad = function () {
            user.getContactInfo()
            .then(function (response) {
                vm.company_image = response.image;
                vm.listed_agent_name = response.listed_agent_name;
                vm.listed_phone_number = response.listed_phone_number;
                vm.listed_email = response.listed_email;
                vm.company_info = response.company_info;
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
        if(vm.search_input.length > 3 || vm.totalbeds !== '' || vm.totalbaths !== '' ||
            vm.pricerangestart !== '' || vm.pricerangestop !== '') {
            vm.homeslist = [];
            $http.get('http://127.0.0.1:8000/homes/', {
                params: {q: vm.search_input, totalbeds: vm.totalbeds, totalbaths: vm.totalbaths,
                        pricerangestart: vm.pricerangestart, pricerangestop: vm.pricerangestop}
        })
        .then(function (response) {
            vm.existingsearchparams = true;
            if (response.data.results.length < 1) {
                vm.nohomesinsearch = true;
            }
            else {
                vm.nohomesinsearch = false;
            }
            $location.path('/search');
            console.log(response.data);
            response.data.results.forEach(function (house) {
                house.price = house.price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
            });
            vm.homeslist = {'response':response.data, 'results': response.data.results};
            vm.search_input = '';
            vm.totalbeds = '';
            vm.totalbaths = '';
            vm.pricerangestart = '';
            vm.pricerangestop = '';
        });
        }
        vm.opensearch = false;
    };

    vm.checkifsearchparams = function () {
        if (!vm.homeslist.results && !vm.existingsearchparams) {
            $location.path('/home');
        }
        else {
            return;
        }
    };

    vm.pageloadhomedetails = function () {
        //this function just grabs the data on page load rather than relying on the reroute function

        vm.home.getlistingdetail(vm.detailhouseid).then(function(response) {
            response.price = response.price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
            vm.listingdetail = response;
            console.log('house detail',response);
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
                return;
            } else {
                vm.current_user = false;
                return;
            }
        }
    };

    vm.getCurrentUser = function () {
        vm.user.getCurrentUser()
        .then(function (data) {
            console.log('current user', data);
            vm.current_user = data;
            vm.current_user.id = data.id;
        });
    };

    // will need to be on the main controller
    vm.login = function () {
        vm.username = vm.username.toLowerCase();
        vm.user.login(vm.username, vm.password)
        .then(function () {
            vm.getCurrentUser();
            $route.reload();
        });
    };

    // will need to be on the main controller
    vm.logout = function () {
            var currpath = $location.path();
            vm.user.logout();
            vm.current_user = false;
            vm.login_clicked = false;
            if (currpath == '/favorites' || currpath == '/profile') {
                vm.reroute('/home');
            }
    };

    vm.checkpasswordmatch = function() {
        vm.passwordlengthvalid = false;
        if (vm.createpassword.length < 8 && vm.createpassword.length !== 0) {
            vm.error = 'Password length must be 8 or more characters!';
        }
        else {
            vm.passwordlengthvalid = true;
        }

        if (vm.passwordlengthvalid === true) {
            if (vm.createpassword !== vm.createconfirmpassword && vm.createpassword !== '' &&
            vm.createconfirmpassword !== '') {
                vm.error = 'Passwords do not match!';
            }
            else {
                vm.error = '';
            }
        }
    };

    vm.createlogin = function() {
        if (vm.createusername.length <= 3) {
            vm.usernametooshort = true;
        }
        else {
            vm.usernametooshort = false;
        }
        if(vm.createpassword == vm.createconfirmpassword && vm.createpassword.length >= 8 &&
            vm.createusername.length > 3 && vm.emailavailable) {
            vm.createusername = vm.createusername.toLowerCase();
            vm.user.createlogin(vm.createusername, vm.createfirstname, vm.createlastname,
                                vm.createemail, vm.createpassword, vm.createphone)
            .then(function() {
                vm.user.login(vm.createusername, vm.createpassword)
                .then(function(response) {
                    vm.createusername = '';
                    vm.createemail = '';
                    vm.createphone = '';
                    vm.getCurrentUser();
                    vm.reroute('/home');
                });
            });
            }
            else {
                return;
            }
    };

    vm.updateprofile = function () {
        vm.user.updateprofile(vm.createfirstname, vm.createlastname, vm.createemail, vm.createphone, vm.current_user.id)
        .then(function (response) {
            vm.createfirstname = '';
            vm.createlastname = '';
            vm.createemail = '';
            vm.createphone = '';
            console.log('profile update successful');
            vm.getCurrentUser();
            vm.editfirstname = false;
            vm.editlastname = false;
            vm.editprofile = false;
            vm.editphone = false;
            vm.editemail = false;
        });
    };

    vm.profile_check_if_logged_in = function () {
        var currpath = $location.path();
        if(!vm.current_user) {
            vm.reroute('/home');
        }
        else {
            return;
        }
    };

    vm.usernameremovespaces = function (string) {
        vm.createusername = string.replace(/\s/g, "");
    };

    vm.passwordremovespaces = function (string) {
        vm.createpassword = string.replace(/\s/g, "");
    };

    vm.checkifuniqueuser = function () {
        vm.usernametooshort = false;
        if (vm.createusername.length < 4) {
            vm.usernameavailable = false;
            vm.error = "";
        }

        if (vm.createusername.length < 4 && vm.createusername.length !== 0) {
            vm.usernametooshort = true;
        }
        else {
            vm.usernametooshort = false;
            if (vm.createusername.length !== 0) {
                vm.user.checkifuniqueuser(vm.createusername.toLowerCase())
                .then(function (response) {
                    if(response.data == "Username already in use!") {
                        vm.error = response.data;
                        vm.usernameavailable = false;
                        vm.usernameunavailable = true;
                    }
                    else {
                        vm.usernameavailable = true;
                        vm.usernameunavailable = false;
                    }
                });
            }
        }
    };

    vm.checkifuniqueemail = function () {
        if (vm.createemail.length < 4) {
            vm.emailavailable = false;
            vm.error = "";
        }

        if (vm.createemail.length >= 4) {
            vm.user.checkifuniqueemail(vm.createemail.toLowerCase())
            .then(function (response) {
                if(response.data == "Email already in use!") {
                    vm.error = response.data;
                    vm.emailavailable = false;
                    vm.emailunavailable = true;
                }
                else {
                    vm.emailavailable = true;
                    vm.emailunavailable = false;
                }
            });
        }
    };

    vm.sendpasswordresetrequest = function () {
        vm.user.sendpasswordresetrequest(vm.passwordresetsendtoemail);
    };

    vm.updatePassword = function () {
        vm.user.updatePassword($routeParams, vm.createpassword)
        .then(function(response) {
            vm.updatePasswordMessage = response;
        });
    };

    // will need to be on the main controller
    vm.getHomesList = function () {
        vm.homespagelist = [];

        vm.home.getHomeListings().then(function (response) {
            response.results.forEach(function (house) {
                house.price = house.price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
            });
            vm.homeslist = {'response':response, 'results': response.results};
        });
    };


    vm.getPremiumHomesList = function () {
        vm.premiumhomepagelist = [];

        vm.home.getPremiumListings().then(function (response) {
            response.results.forEach(function (house) {
                house.price = house.price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
            });
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
                response.results.forEach(function (house) {
                    house.price = house.price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                });
                if (response.results.length < 1) {
                    vm.favoriteslist.results = false;
                }
                else {
                    vm.favoriteslist.results = vm.favoriteslist.concat(response.results);
                    vm.favoriteslist.response = response;
                }
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
