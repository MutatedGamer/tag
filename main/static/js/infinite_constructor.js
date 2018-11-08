var infinite = new Waypoint.Infinite({
	element: $('.infinite-container')[0],
		context: $('body'),
		onBeforePageLoad: function () {
			$('.loading').show();
		},
		onAfterPageLoad: function ($items) {
			$('.loading').hide();
		}
	});

