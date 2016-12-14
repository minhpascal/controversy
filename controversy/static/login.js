if (navigator.userAgent.indexOf('MSIE') !== -1 || navigator.appVersion.indexOf('Trident/') > 0) {
	window.location.replace('not-supported');
}

document.getElementsByTagName('form')[0].style.display = 'block';

if (!window.jQuery) {
	document.getElementsByTagName('form')[0].style.display = 'none';
	document.getElementById('anon_login').style.display = 'none';
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
	}, 'https://api.github.com/repos/SXibolet/controversy/issues');
});


function getJSON(callback, failure_callback, url) { 
	$.getJSON(url, function(data) {
		callback(data);
	}).fail(function() {
		failure_callback();	
	});
}



