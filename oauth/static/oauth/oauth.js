window.fbAsyncInit = function() {
    FB.init({
        appId      : '264078186960926',
        xfbml      : true,
        version    : 'v2.5'
    });
    startPostFb();
};

(function(d, s, id){
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) {return;}
    js = d.createElement(s); js.id = id;
    js.src = "//connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

function startPostFb() {
    FB.getLoginStatus(function(response) {
        if (response.status === 'connected') {
            sendOauthResponse(FB.getAuthResponse());
        }
        else {
            FB.login();
        }
    });
}

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function sendOauthResponse(response) {
    $.ajax({
        type: 'post', 
        url: '/oauth/facebook/auth',
        data: JSON.stringify(response),
        headers: {
            'content-type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        }
    });
}
