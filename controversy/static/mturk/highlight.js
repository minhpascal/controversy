$(document).ready(function() {

});

function toggleControversial(i, el) {
	if ($.inArray(i, controversial) !== -1) {
		// ``i`` is in ``controversial``
		controversial = $.grep(controversial, function(x) {
			return x != i;
		});

		$(el).removeClass('controversial');
	} else {
		controversial.push(i);
		$(el).addClass('controversial');
	}
}

$("#submit").click(function() {
	console.log('%c not ready ', 'background: #222; color: #bada55');
})
