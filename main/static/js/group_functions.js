function makeAdmin(pk) {
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
		url: $add_admin_url, // url where to submit the request
		type : "POST", // type of action POST || GET
		dataType : 'json', // data type
		data : { 'user-id': pk, 'group': $group_pk },
		success : function(result) {
			console.log(result);
			if (result['success']) {
				$('#add-admin-search').trigger('keyup');
			}
		},
	});
	
};

function removeAdmin(pk) {
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
		url: $remove_admin_url, // url where to submit the request
		type : "POST", // type of action POST || GET
		dataType : 'json', // data type
		data : { 'user-id': pk, 'group': $group_pk },
		success : function(result) {
			console.log(result);
			if (result['success']) {
				$('#add-admin-search').trigger('keyup');
			}
		},
	});
	
};




function changeOwner(pk) {
	var r = confirm('Are you sure you want to change the owner of the group to this person? This action cannot be undone.');
	if (r==true) {
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
			url: $change_owner_url, // url where to submit the request
			type : "POST", // type of action POST || GET
			dataType : 'json', // data type
			data : { 'user-id': pk, 'group': $group_pk },
			success : function(result) {
				console.log(result);
				if (result['success']) {
					window.location.href = $groups_url;
				}
			},
		});
	};
	
};

$('#make-unmoderated').click( function(e) {
	e.preventDefault();
	var r = confirm("Are you sure you want to make the group " + $group_name + " unmoderated?\nThis action cannot be undone, and all unapproved posts will automatically be approved.");
	if (r==true) {
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
			url: $make_unmod_url, // url where to submit the request
			type : "POST", // type of action POST || GET
			dataType : 'json', // data type
			data : { 'group': $group_pk},
			success : function(result) {
				console.log(result);
				if (result['success']) {
					window.location.href = $group_url;
				}
			},
		});
	};
	return false;
});

$('#delete-group').click( function(e) {
	e.preventDefault();
	var r = confirm("Are you sure you want to delete the group " +  $group_name + "? \nThis action cannot be reversed, and all posts in the group will be lost forever.");
	if (r==true) {
		var r = confirm('If you click "OK" then ' + $group_name + ' and all of its posts will forever be gone. Are you sure you want to do this?');
		if (r==true) {
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
                url: $delete_group_url, // url where to submit the request
                type : "POST", // type of action POST || GET
                dataType : 'json', // data type
                data : { 'group': $group_pk },
                success : function(result) {
					console.log(result);
					if (result['success']) {
						window.location.href = $groups_url;
					}
				},
			});
		};
	};
	return false;
});
