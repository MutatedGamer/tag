

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
