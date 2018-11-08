function tag(pk) {
	$("#tag-post-id").attr('value', pk);
	$("#tag_modal").modal("show");
};

function tagFriendAJAX(post_pk, friend_pk) {
	function csrfSafeMethod(method) {
		// these HTTP methods do not require CSRF protection
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}
	// send ajax
	$.ajax({
		beforeSend: function(xhr, settings) {
				if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
					xhr.setRequestHeader("X-CSRFToken", csrftoken);
				}
			},
		url: $tag_url, // url where to submit the request
		type : "POST", // type of action POST || GET
		dataType : 'json', // data type
		data : { 'post-id': post_pk, 'friend-pk': friend_pk },
		success : function(result) {
			$('#tag-search').keyup();
			$('#tag-post-' + post_pk).text(result['new_count'])
		},
	});
};

$('#tag_modal').on('hidden.bs.modal', function(e) {
	$('#tag-search').val('');
	$('#tag-search-result-container').html('');
});

$('#tag_modal').on('shown.bs.modal', function(e) {
	$('#tag-search').keyup();
});

function like(pk) {
	function csrfSafeMethod(method) {
		// these HTTP methods do not require CSRF protection
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}
	// send ajax
	$.ajax({
		beforeSend: function(xhr, settings) {
				if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
					xhr.setRequestHeader("X-CSRFToken", csrftoken);
				}
			},
		url: $like_url, // url where to submit the request
		type : "POST", // type of action POST || GET
		dataType : 'json', // data type
		data : { 'post-id': pk },
		success : function(result) {
			if (result['result'] == 'liked') {
				$('#like-button-' + pk).css('color', 'green');
				$('#like-button-' + pk).addClass('liked');
				$('#like-post-' + pk).text(result['new_count'])
			}
			else {
				$('#like-button-' + pk).css('color', 'grey');
				$('#like-post-' + pk).text(result['new_count'])
			};
		},
	});
};

function reply(pk) {
	function csrfSafeMethod(method) {
		// these HTTP methods do not require CSRF protection
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}
	// send ajax
	$.ajax({
		beforeSend: function(xhr, settings) {
				if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
					xhr.setRequestHeader("X-CSRFToken", csrftoken);
				}
			},
		url: $make_reply_url , // url where to submit the request
		type : "POST", // type of action POST || GET
		dataType : 'html', // data type
		data : { 'post-id': pk },
		success : function(result) {
      $('#reply-modal-content').html(result);
      $('#reply_modal').modal('show');
    },
	});
};


function star(pk) {
	function csrfSafeMethod(method) {
		// these HTTP methods do not require CSRF protection
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}
	// send ajax
	$.ajax({
		beforeSend: function(xhr, settings) {
				if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
					xhr.setRequestHeader("X-CSRFToken", csrftoken);
				}
			},
		url: $star_url, // url where to submit the request
		type : "POST", // type of action POST || GET
		dataType : 'json', // data type
		data : { 'post-id': pk },
		success : function(result) {
			if (result['result'] == 'starred') {
				$('#star-button-' + pk).css('color', 'gold');
			}
			else {
				$('#star-button-' + pk).css('color', 'grey');
			};
		},
	});
};

function comment(pk) {
	var form = $('#add-comment-' + pk);
		form.fadeIn(250);
}

function showHideParent(pk) {
  var $container = $('#parent-container-' + pk);
  var $button = $('#show-hide-parent-button-' + pk);
  if ($container.is(':hidden')) {
    $container.fadeIn(250);
    $button.html('&nbsp;&nbsp;&nbsp;[hide original post]');
  }
  else {
    $container.fadeOut(250);
    $button.html('&nbsp;&nbsp;&nbsp;[show original post]');
  };
    
};

$('.add-comment-form').submit(function(e) {
	e.preventDefault();
	var $pk = $(this).attr('data-url');

	function csrfSafeMethod(method) {
		// these HTTP methods do not require CSRF protection
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}
	// send ajax
	$.ajax({
		beforeSend: function(xhr, settings) {
				if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
					xhr.setRequestHeader("X-CSRFToken", csrftoken);
				}
			},
		url: $comment_url, // url where to submit the request
		type : "POST", // type of action POST || GET
		dataType : 'html', // data type
		data : { 'post-id': $(this).attr('data-url'), 'body': $(this).find("textarea").val() },
		success : function(data) {
			var toAppend = $('#comment-container-' + $pk);
      if (toAppend.length != 0) {
			  toAppend.html(data);
      } else {
        location.reload();
      }

		},
	});
	$(this).find("textarea").val('') 

});

$(document).on('submit', '#reply-form', function(e) {
  e.preventDefault(); // avoid to execute the actual submit of the form.
  var form = $(this);
  var url = form.attr('action');

  $.ajax({
         type: "POST",
         url: url,
         data: form.serialize(), // serializes the form's elements.
         success: function(data)
         {
           if (data.success) {
             $('#reply-modal-body').html('<div class="alert alert-success">' + data.message + '</div>');
           }
           else {

             $('#reply-modal-body').html('<div class="alert alert-danger"> Something went wrong!</div>');
           };
         }
       });

});
