

// This is called with the results from from FB.getLoginStatus().
  function statusChangeCallback(response) {
    console.log('statusChangeCallback');
    console.log(response);
    // The response object is returned with a status field that lets the
    // app know the current login status of the person.
    // Full docs on the response object can be found in the documentation
    // for FB.getLoginStatus().
    var login_area = document.getElementById("login-area");
    if (response.status === 'connected') {
      // Logged into your app and Facebook.
      // alert(response.authResponse.userID)
      // window.location = "main.html";
      user_id = response.authResponse.userID;
      login_area.innerHTML = '<div class="dropdown" style="display: inline-block;">\
                                <button type="button" class="btn btn-outline-notifications btn-sm dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"> \
                                  <i style="padding-right:5px;" class="fas fa-bell fa-lg"></i><span class="badge badge-pill badge-danger"></span>\
                                </button>\
                                <div id="notifications" class="dropdown-menu dropdown-menu-right" aria-labelledby="dropdownMenuButton">\
                                  <a class="dropdown-item" href="#">Super duper long notificaiton grdgdtf gfd gfd gdf gfd gfd gdfg dfg fdg fdg fdg fdg </a>\
                                  <div class="dropdown-divider"></div>\
                                  <a class="dropdown-item" href="#">Another action</a>\
                                  <div class="dropdown-divider"></div>\
                                  <a class="dropdown-item" href="#">Something else here</a>\
                                </div>\
                              </div>\
                              <div class="btn-group" role="group" style="padding-left: 1px; display: inline-block;">\
                                <button type="button" class="btn btn-outline-danger btn-sm" data-toggle="modal" data-target="#settings_overlay">\
                                  <i class="fas fa-cog fa-lg"></i>\
                                </button>\
                                <button id="login-button" type="button" class="btn btn-outline-danger btn-sm" onclick="logout()" style="margin-left:-5px">\
                                  <i class="fa fa-sign-out-alt fa-lg" aria-hidden="true"></i>\
                                </button>\
                              </div>\
                              <div style="clear: both;"></div>';
    } else {
      // The person is not logged into your app or we are unable to tell.
      // document.getElementById('status').innerHTML = 'Please log ' +
        // 'into this app.';
      login_area.innerHTML = '<div class="fb-login-button" data-max-rows="1" data-size="medium" data-button-type="continue_with" data-show-faces="false" data-auto-logout-link="false" scope="user_friends" data-use-continue-as="false" onlogin="refresh()"></div>';
      FB.XFBML.parse();
    }
  }



  window.fbAsyncInit = function() {
    FB.init({
      appId      : appid,
      cookie     : true,  // enable cookies to allow the server to access
                          // the session
      xfbml      : true,  // parse social plugins on this page
      version    : 'v3.0', // use graph api version 2.8
      status     : true
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

  // Load the SDK asynchronously
  (function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src = "https://connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
  }(document, 'script', 'facebook-jssdk'));


  function logout() {
    FB.logout(function(response) {
      location.reload(); 
    });
  }

  function getFriends() {
    FB.api("/me/friends", function(response) {
      console.log('friends');
      console.log(response);
      for (var i = 0; i < response.data.length; i++) {
        alert(response.data[i].id);
      }
    });
  }

function refresh() {
  location.reload(); 
}