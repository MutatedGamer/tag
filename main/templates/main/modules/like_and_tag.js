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
		url: '{% url "tag-friend" %}', // url where to submit the request
		type : "POST", // type of action POST || GET
		dataType : 'json', // data type
		data : { 'post-id': post_pk, 'friend-pk': friend_pk },
		success : function(result) {
			$('#tag-search').keyup();
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
		url: '{% url "like-post" %}', // url where to submit the request
		type : "POST", // type of action POST || GET
		dataType : 'json', // data type
		data : { 'post-id': pk },
		success : function(result) {
			if (result['result'] == 'liked') {
				$('#like-button-' + pk).css('color', 'green');
				$('#like-button-' + pk).addClass('liked');
				$('#post-' + pk).text(result['new_count'])
			}
			else {
				$('#like-button-' + pk).css('color', 'grey');
				$('#post-' + pk).text(result['new_count'])
			};
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
		url: '{% url "star-post" %}', // url where to submit the request
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
		url: '{% url "add-comment" %}', // url where to submit the request
		type : "POST", // type of action POST || GET
		dataType : 'html', // data type
		data : { 'post-id': $(this).attr('data-url'), 'body': $(this).find("textarea").val() },
		success : function(data) {
			var toAppend = $('#comment-container-' + $pk);
			toAppend.html(data);

		},
	});
	$(this).find("textarea").val('') 

});

