if (navigator.userAgent.indexOf('MSIE') !== -1 || navigator.appVersion.indexOf('Trident/') > 0) {
	window.location.replace('not-supported');
}

document.getElementsByTagName('form')[0].style.display = 'block';

if (!window.jQuery) {
	document.getElementsByTagName('form')[0].style.display = 'none';
} else {
	var isWebKit = 'WebkitAppearance' in document.documentElement.style;
	var isSafari = (navigator.userAgent.indexOf('Safari') != -1 && navigator.userAgent.indexOf('Chrome') == -1);
	if (isWebKit) {
		$.ajax({url: '/set/webkit'});
	}
	if (isSafari) {
		$.ajax({url: '/set/safari'});
	}
}

$(document).ready(function() {
	getJSON(function(d) {
		issues = d.length;
		$("#loading_bugs").hide();
		$("#n_bugs")
			.show()
			.text(issues);
		$("#bugs_a").text('Report a bug')
	}, function() {
		issues = '?';
	}, 'https://api.github.com/repos/gdyer/controversy/issues');
});


function getJSON(callback, failure_callback, url) { 
	$.getJSON(url, function(data) {
		callback(data);
	}).fail(function() {
		failure_callback();	
	});
}



