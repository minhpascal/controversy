var cApp = angular.module('Account', []);
cApp.controller('IssuesController', function($scope, $http, $location, $anchorScroll) {
	$scope.issues_loaded = false;
	$http.get('https://api.github.com/repos/SXibolet/controversy/issues')
	.success(function(res) {
		$scope.issues = res;
		$scope.issues_loaded = true;
		if ($location.search().bug) {
			$location.hash('bugs');
			$anchorScroll();
		}
	})
	.error(function(res) {
		console.error('problem loading issues')	
	});
});
