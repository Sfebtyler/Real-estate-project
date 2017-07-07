window.onscroll = function () {
    sessionStorage['cur_pos'] = $(window).scrollTop()
}

$(document).ready(function () {

    open_search = document.getElementById('open_search');
    search_modal = document.getElementById('search_modal');
    modal = document.getElementById('modal');
    login_modal = document.getElementById('page_login')
    login_modal_wrapper = document.getElementById('login_wrapper')
    open_login = document.getElementById('open_login')
    login_logout_next = window.location.pathname
    login_next = document.getElementById('login_next')
    next_page = document.getElementsByClassName('next')
    next = document.location
    login_next = ''
    logout_next = ''
    username = document.getElementById("create__username")
    usernametooshort = document.getElementById("create__usernametooshort")

    var i;
    for (i = 0; i < next_page.length; i++) {
        next_page[i].value = next;
    }

    if (sessionStorage['current_window'] == window.location) {
        window.scrollTo(0, parseInt(sessionStorage['cur_pos']));
    }

//    used to determine if the current page is that same as the page your were just on and then scroll accordingly
//    with the function above
    sessionStorage['current_window'] = window.location

    //  setting login/logout next path
    login_next.value = login_logout_next
    logout_next.value = login_logout_next



//search modal
    var toggled = false;

     function openSearchModal() {
         toggled = true;
         search_modal.style.display = 'flex';
     }

     function closeSearchModal() {
         toggled = false;
         search_modal.style.display = 'none';
     }
     open_search.onclick = function(e) {
         e.stopPropagation();
         openSearchModal();
     }

     close_search.onclick = function() {
         closeSearchModal();
     }

     window.onclick = function (e) {
         if (e.target == modal || $.contains(modal, e.target)) {
         }
         else {
             closeSearchModal();
         }
     }


    //login modal
      var logintoggle = false;

    function openLoginModal() {
        logintoggle = true;
        login_modal_wrapper.style.display = 'flex';
    }

    function closeLoginModal() {
        logintoggle = false;
        login_modal_wrapper.style.display = 'none';
    }
    open_login.onclick = function(e) {
        e.stopPropagation();
        openLoginModal();
    }

    close_login.onclick = function() {
        closeLoginModal();
    }

    window.onclick = function (e) {
        if (e.target == login_modal_wrapper || $.contains(login_modal_wrapper, e.target)) {
        }
        else {
            closeModal();
        }
    }

});
