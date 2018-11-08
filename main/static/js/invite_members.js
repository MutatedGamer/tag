function inviteMemberAJAX(friend_pk) {
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
			url: $invite_member_url, // url where to submit the request
			type : "POST", // type of action POST || GET
			dataType : 'json', // data type
			data : { 'friend-pk': friend_pk },
			success : function(result) {
				// Display invited messages
				$message = $('<div class="col-12 alert-success">Invited!</div>')
				$('#invite-member-body').prepend($message);
				$message.fadeOut(3000);
			},
		});
	};
