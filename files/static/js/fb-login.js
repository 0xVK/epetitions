function getUserData(resp) {
  
    FB.api('/me', 
           {fields: 'name,email, first_name, last_name, link, gender, id, locale'},
           function (response) {
              $.ajax({
                type: 'POST',
                url: '/fb_login/',
                async: false,
                data: 'ajaxData=' + JSON.stringify(response) + '&token=' + JSON.stringify(resp['authResponse']['accessToken']),
                
                success: function (result) {
                   location.reload();
                }
            })
        });
}

window.fbAsyncInit = function() {
    FB.init({
        appId      : '1811792615511023',
        xfbml      : true,
        version    : 'v2.11'
    });
};

(function(d, s, id){
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) {return;}
    js = d.createElement(s); js.id = id;
    js.src = "//connect.facebook.com/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

document.getElementById('fb-login-btn').addEventListener('click', function() {
    
  FB.getLoginStatus(function(response) {
    if (response.status === 'connected') {
      console.log(JSON.stringify(response));
        getUserData(response);
    } else {
        FB.login(function(response) {
        if (response.authResponse) {
          //user just authorized your app
          getUserData(response);
        }
        }, {scope: 'public_profile,email'});
    }
    });

}, false);
