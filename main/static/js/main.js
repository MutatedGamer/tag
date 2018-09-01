
// CHANGE ACTIVE BUTTON ON CLICK//
// Get the container element
var btnContainer = document.getElementById("navbar-left");

// Get all buttons with class="btn" inside the container
var btns = btnContainer.getElementsByClassName("nav-link");

// Loop through the buttons and add the active class to the current/clicked button
for (var i = 0; i < btns.length; i++) {
  btns[i].addEventListener("click", function() {
    var current = document.getElementsByClassName("active");
    current[0].className = current[0].className.replace(" active", "");
    this.className += " active";
  });
} 


//AUTO-EXPAND COMPOSE BOX//
$(function() {
  $('#compose-box').on('keyup paste', function() {
    var $el = $(this),
        offset = $el.innerHeight() - $el.height();

    if ($el.innerHeight < this.scrollHeight) {
      //Grow the field if scroll height is smaller
      $el.height(this.scrollHeight - offset);
    } else {
      //Shrink the field and then re-set it to the scroll height in case it needs to shrink
      $el.height(1);
      $el.height(this.scrollHeight - offset);
    }
  });
});