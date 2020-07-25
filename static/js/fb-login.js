function getQueryVariable(variable) {
  var query = window.location.search.substring(1);
  var vars = query.split("&");
  for (var i=0;i<vars.length;i++) {
    var pair = vars[i].split("=");
    if (pair[0] == variable) {
      return pair[1];
    }
  } 
  console.log('Url param: ' + variable + ' not found');
}

function getUserData(resp) {
  
    FB.api('/me', 
           {fields: 'name,email, first_name, last_name, link, gender, id, locale'},
           function (response) {
              $.ajax({
                type: 'POST',
                url: '/fb_login/',
                async: false,
                data: 'ajaxData=' + JSON.stringify(response) + '&token=' + JSON.stringify(resp['authResponse']['accessToken']) + '&next=' + getQueryVariable("next"),
                
                success: function (result) {
                   console.log(result['status']);
                   if (result['code'] == 102){
                     alert (result['status']);
                   } else {
                     if (getQueryVariable("next")){
                          window.location.href = getQueryVariable("next"); 
                         } else {
                          location.reload();
                         }
                   }
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


function FB_Login() {
  
  FB.getLoginStatus(function(response) {
    if (response.status === 'connected') {
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

};

window.onload = function () {
   document.getElementById("fb-login-btn-h").onclick=FB_Login;
};