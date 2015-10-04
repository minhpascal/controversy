var cApp = angular.module('Account', []);
cApp.controller('IssuesController', function($scope, $http) {
	$scope.issues_loaded = false;
	$http.get('https://api.github.com/repos/gdyer/controversy/issues')
	.success(function(res) {
		$scope.issues = res;
		$scope.issues_loaded = true;
		console.log(res);
	})
	.error(function(res) {
		console.error('problem loading issues')	
	});
});
