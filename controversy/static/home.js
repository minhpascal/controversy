var cApp = angular.module('Home', ['ngRoute', 'ngSanitize', 'angular-loading-bar', 'ngAnimate']);
var ERROR_MESSAGES = {
	'no-articles' : 'Despite our best efforts, we could not find any recently published English articles with that keyword. May we interest you in another try?',
	'our-fault' : 'Well, this is awkward; we messed up. Check current bugs. We were automatically sent an SMS about this error, but please report it if it\'s an unknown problem.',
	'not-logged-in' : 'You logged out in another window or a server update was just pushed! Please refresh the page, and log in again.',
	'failed-to-parse' : 'There was a malformed article result that broke this response. Please try a different keyword, and file a bug.'
};

cApp.config(['cfpLoadingBarProvider', function(cfpLoadingBarProvider) {
	cfpLoadingBarProvider.includeSpinner = false;
}])

cApp.run(function($rootScope) {
	$rootScope.keyword = '';
	$rootScope.last_query = '';
	$rootScope.can_query = true;
	$rootScope.setError = function(code) {
		var e = code in ERROR_MESSAGES;
		$rootScope.error = {
			'message' : (e) ? ERROR_MESSAGES[code] : ERROR_MESSAGES['our-fault'],
			'code' : (e) ? code : 'our-fault'
		}
	}
	$rootScope.article = function(index) {
		return ($rootScope.json) ? $rootScope.json[index] : null;
	};
});

cApp.config(function ($routeProvider) {
	$routeProvider
	.when('/', {
		templateUrl : 'partial/search.html',
		controller : 'SearchController'
	})
	.when('/results', {
		templateUrl : 'partial/results.html',
		controller : 'ResultsController'
	})
	.when('/results/:article/:sentence', {
		templateUrl : 'partial/tweets.html',
		controller : 'TweetsController'
	})
	.when('/results/:article', {
		templateUrl : 'partial/read.html',
		controller : 'ReadController'
	})
	.when('/error', {
		templateUrl : 'partial/error.html',
		controller : 'ErrorController'
	})
	.when('/trends/:keyword', {
		templateUrl : 'partial/trend.html',
		controller : 'TrendController'
	})
	.otherwise({
		redirectTo: '/'
	});
});

cApp.controller('SearchController', function($scope, $http, $rootScope, $location) {
	var SET_OPACITY = function(o) {
		$rootScope.results_style = {'opacity' : o };
	}
	$scope.testing_js = true;
	$scope.button_value = 'query';

	$scope.$watch(function() {
		return $rootScope.keyword;
	}, function() {
		$rootScope.can_query = ($rootScope.keyword && $rootScope.keyword.length > 0) && ($rootScope.keyword.localeCompare($rootScope.last_query) != 0);
		SET_OPACITY(($rootScope.can_query) ? 0.5 : 1.0);

		if (!$rootScope.keyword) return;
		$http.get('/api/trend/' + $rootScope.keyword)
			.success(function(res) {
				$scope.trend_available = !(res['error'] || res['result'].length < 4);
			}).error(function(res) {
				return;
			});
	}, true);

	function broken(m) {
		$scope.trending = m || "<trending queries are unavailable>";
	}


	$http.get('/api/trend')
	.success(function(res) {
		if (res['error']) {
			broken();	
			return;
		}
		$scope.trending = res['result']['top-5'];
		$scope.traffic_dist = res['result']['trending'];
		$scope.controversial = res['result']['controversial'];
	})
	.error(function(res) {
		broken();
	});

	$scope.clear = function() {
		$rootScope.json = $rootScope.error = $rootScope.keyword = $rootScope.last_query = null;
		$rootScope.is_loading = false;
		$location.path('/');
	}

	$scope.submit = function() {
		if ($rootScope.json && ($rootScope.last_query.localeCompare($rootScope.keyword) === 0)) {
			$location.path('/results');
		}
		if ($rootScope.is_loading || !$rootScope.can_query) {
			return;
		}

		$rootScope.error = null;
		$rootScope.last_query = $rootScope.keyword; 
		$scope.button_value = 'querying...';
		$rootScope.is_loading = true;

		function handleError(message) {
			$rootScope.is_loading = false;  
			$rootScope.setError(message);
			$rootScope.json = null;
			$scope.button_value = 'problems...';
			$location.path('/error');
		}

		var call = '/api?q=' + $rootScope.keyword;
		console.log('querying ==> ' + call);

		$http.get(call).
			success(function(res) {
				$rootScope.json = res['result'];
				$rootScope.is_loading = false;  
				if (res['error']) {
					handleError(res['message']);
					return;
				}
				$rootScope.can_query = true;
				$scope.button_value = 'query';
				if ($location.path() == '/results') {
					SET_OPACITY(1.0);
				} else {
					$location.path('/results');
				}
			}).
		error(function(res) {
			handleError(res['message']);
		});
	};

	$scope.$watch(function () { return $rootScope.keyword; },
		function (value) {

		}
	);
});

cApp.controller('ResultsController', function($scope, $rootScope, $location, $window, $http) {
	$window.scrollTo(0, 0);
	if (!$rootScope.json) {
		$location.path('/');
		return;
	}

	$scope.readArticle = function(index) {
		$rootScope.article(index);
	}
});

cApp.controller('ErrorController', function($scope, $rootScope, $location) {
	if (!$rootScope.error) {
		$location.path('/');
	}

	$scope.goHome = function() {
		$location.path('/');
	};

	$scope.goToAccount = function() {
	console.log('goAccount!');
		window.location.href = 'account#?bug';
	};
});

cApp.controller('ReadController', function($scope, $rootScope, $location, $routeParams, $window) {
	$window.scrollTo(0, 0);
	$scope.articleIndex = parseInt($routeParams.article);
	if (!$scope.article || !$rootScope.json) {
		$location.path('/');
		return;
	}

	$scope.article = $rootScope.article($scope.articleIndex);
	$scope.nextExists = $scope.articleIndex < $rootScope.json.length - 1;
	$scope.previousExists = $scope.articleIndex != 0;

	$scope.change = function(i) {
		$scope.articleIndex += i;
		$location.path('results/' + $scope.articleIndex);
		$location.hash('right-header');
	};

	var value = $window.innerWidth;
	$scope.lim = 130;
	if (value < 500)
		$scope.lim = 20;
	else if (value < 600)
		$scope.lim = 40;
	else if (value < 750)
		$scope.lim = 50;

	$scope.highlight = function(corpus, needles) {
		var i = -1;
		var re = new RegExp(needles.map(function(x) {
			return x['text']
		}).join('|'), 'gi');
		corpus = corpus.replace(re, function(matched) {
			i++; 
			return "<b><a href='#results/" + $routeParams.article + '/' + i + "'>" + matched + "</a></b>";
		});

		return corpus;
	};

});


cApp.controller('TweetsController', function($scope, $rootScope, $location, $routeParams, $window) {
	$window.scrollTo(0, 0);
	$scope.sentenceIndex = parseInt($routeParams.sentence);
	$scope.articleIndex = $routeParams.article;
	var articles = $rootScope.article([$scope.articleIndex]);
	if (!articles) {
		$location.path('/');
		return;
	}

	$scope.sentence = articles['sentences'][$scope.sentenceIndex];
	$scope.nextExists = $scope.sentenceIndex < articles['sentences'].length - 1;
	$scope.previousExists = $scope.sentenceIndex != 0;

	$scope.change = function(i) {
		$scope.sentenceIndex += i;
		$location.path('results/' + $scope.articleIndex + '/' + $scope.sentenceIndex);
		$location.hash('right-header');
	};

});


cApp.controller('TrendController', function($rootScope, $location, $window) {
	if (!$rootScope.keyword) {
		$location.path('/');
		return;
	}

	$window.scrollTo(0, 0);
});


