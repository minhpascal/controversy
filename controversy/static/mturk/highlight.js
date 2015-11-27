var CONFIRMED_HIGHLIGHTS = false;
var STARTED_READING;
var count = parseInt(minimum_time / 1000);
var counter = setInterval(function() {timer();}, 1000);

function timer() {
	count -= 1
	if (count <= 0) {
		clearInterval(counter);
		$("#time_left span").html("submit <b>whenever</b> you're ready");
		$("#time_left").addClass('alert-success');
		setTimeout(function() {
			updateCanSubmit();
		}, 1500);
		setTimeout(function() {
			markAvailable();
		}, 30000);

		return;	
	}

	$("#time_left span").html('<b>' + count + '</b> ' + ((count === 1) ? 'second' : 'seconds') + ' until you can submit');
}

$(document).ready(function() {
	STARTED_READING = new Date().getTime();
	setTimeout(function() {
		updateCanSubmit();
	}, minimum_time);
});

$(window).bind('beforeunload', function() {
	markAvailable();
});

function markAvailable() {
	performRequest('mark_available',
			function(data) {
				console.log('marked available')
			}, function(data) {
				console.log(data);
			});
}

function performRequest(uri, callback, failure_callback) {
	$.getJSON(uri,
		function(data) {
			callback(data);
		}).fail(function(jqxhr, textStatus, error) {
			failure_callback($.parseJSON(jqxhr.responseText));
	});
};

function toggleControversial(i, el) {
	if ($.inArray(i, controversial) !== -1) {
		controversial = $.grep(controversial, function(x) {
			return x != i;
		});

		$(el).removeClass('controversial');
	} else {
		controversial.push(i);
		$(el)
			.addClass('controversial')
			.prop('title', 'currently controversial');
	}

	updateCanSubmit();
}

function pastMinTime() {
	var now = new Date();
	var elapsed_ms = now.getTime() - STARTED_READING;
	return (elapsed_ms > minimum_time);
}


function updateCanSubmit() {
	var n_highlights = controversial.length;
	if (n_highlights == 0 || !pastMinTime()) {
		disable('#submit');
	} else {
		enable('#submit');
	}
}

function showError(message) {
	$("#error").text(message);
	setTimeout(function() {
		$("#error").text('');
	}, 3000);
}

function disable(el) {
	$(el)
		.prop('disabled', true)
		.addClass('disabled');
}

function enable(el) {
	$(el)
		.prop('disabled', false)
		.removeClass('disabled');
}

function submitComplete() {

}

function submitSuccess(data) {
	$("#bot_bar img").hide();
	console.log(data);
}

function submitFailure(data) {
	$("#bot_bar img").hide();
	showError(data['message']);
}

$("#submit").click(function() {
	// these checks will be done server-side too. They are duplicated here to reduce strain on the server.
	if (!pastMinTime()) {
		showError("your words per minute is too high");
		return;
	}

	var n_highlights = controversial.length;
	if (n_highlights === 0) {
		showError("no highlights");
		return;
	}

	if (n_highlights > n_sentences) {
		showError('invalid # of highlights!');
		enable('#full_article');
		return;
	}

	for (var i = n_highlights - 1; i >= 0; i -= 1) {
		var ei = controversial[i];
		if (ei < 0 || ei > n_sentences) {
			showError('invalid sentence indices!');
			return;
		}
	}

	if (n_highlights > (0.8 * n_sentences)) {
		showError("too many sentences highlighted");
		return;
	}

	if (n_highlights < (n_sentences * 0.1) && !CONFIRMED_HIGHLIGHTS) {
		showError("are you sure you've highlighted all controversial sentences? Submit again to confirm.");
		CONFIRMED_HIGHLIGHTS = true;
		return;
	}

	if (n_highlights > (0.5 * n_sentences) && !CONFIRMED_HIGHLIGHTS) {
		showError("are you sure you've highlighted only controversial sentences? Submit again to confirm.");
		CONFIRMED_HIGHLIGHTS = true;
		return	
	}


	controversial.sort();
	var uri = 'submit?checked=' + controversial.join();
	$("#bot_bar img").show();
	performRequest(uri, submitSuccess, submitFailure);
})
