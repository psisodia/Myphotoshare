(function(d, s, id) {
  var js, fjs = d.getElementsByTagName(s)[0];
  if (d.getElementById(id)) return;
  js = d.createElement(s); js.id = id;
  js.src = "//connect.facebook.net/en_US/sdk.js#xfbml=1&appId=1530401767181319&version=v2.0";
  fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));


// This is called with the results from from FB.getLoginStatus().
function statusChangeCallback(response) {
  console.log('statusChangeCallback');
  console.log(response);

  // The response object is returned with a status field that lets the
  // app know the current login status of the person.
  // Full docs on the response object can be found in the documentation
  // for FB.getLoginStatus().

  if (response.status === 'connected') {
    testAPI();
  } else if (response.status === 'not_authorized') {
    // The person is logged into Facebook, but not your app.
    document.getElementById('status').innerHTML = 'Please log ' +
      'into this app.';
  } else {
    // The person is not logged into Facebook, so we're not sure if
    // they are logged into this app or not.
    document.getElementById('status').innerHTML = 'Please log ' +
      'into Facebook.';
  }
}

// This function is called when someone finishes with the Login
// Button.  See the onlogin handler attached to it in the sample
// code below.
function checkLoginState() {
  FB.getLoginStatus(function(response) {
    statusChangeCallback(response);
    if (response.status === 'connected') {

      FB.api('/me', function(response) {
        var javsacript_json_object = JSON.stringify(response);

        $.ajax(
        {
          type: 'POST',
          url: "/process_facebook_login",
          data: {
            fbdata: javsacript_json_object
          },
        }).done(function(data) {
          localStorage.setItem['fb'] = true;
          console.log(data);
          location.replace('/upload_album');
        });
        console.log(JSON.stringify(response));
      });
    }
  });
}

window.fbAsyncInit = function() {
  FB.init({
    appId      : '{1530401767181319}',
    cookie     : true,  // enable cookies to allow the server to access 
                        // the session
    xfbml      : true,  // parse social plugins on this page
    version    : 'v2.0' // use version 2.0
  });

  // Now that we've initialized the JavaScript SDK, we call 
  // FB.getLoginStatus().  This function gets the state of the
  // person visiting this page and can return one of three states to
  // the callback you provide.  They can be:
  //
  // 1. Logged into your app ('connected')
  // 2. Logged into Facebook, but not your app ('not_authorized')
  // 3. Not logged into Facebook and can't tell if they are logged into
  //    your app or not.
  //
  // These three cases are handled in the callback function.

  FB.getLoginStatus(function(response) {
    statusChangeCallback(response);
  });

};


// Here we run a very simple test of the Graph API after login is
// successful.  See statusChangeCallback() for when this call is made.
function testAPI() {
  console.log('Welcome!  Fetching your information.... ');
  localStorage.setItem('fb', true);
  FB.api('/me', function(response) {
    var javsacript_json_object = JSON.stringify(response);
  });

}

function logoutFB(){
  FB.logout(function(){
    console.log("facebook logout");
  })
}

$(document).ready(function (){
  $("#logout").click(function(){
    if (localStorage.getItem('fb') === "true"){
      logoutFB();
    }
  })
})