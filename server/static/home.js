var cApp = angular.module('Home', ['ngRoute', 'ngSanitize']);
var ERROR_MESSAGES = {
  'no-articles' : 'Despite our best efforts, we simply could not find any articles with that keyword. May we interest you in another try?',
  'our-fault' : 'Well, this is akward; we messed up. Please file a bug at github.com/gdyer/controversy/issues.',
  'not-logged-in' : 'A server update was just pushed! Please refresh the page and log in again.'
};

cApp.run(function($rootScope) {
  $rootScope.keyword = '';
  $rootScope.last_query = '';
  $rootScope.can_query = true;
  $rootScope.setError = function(code) {
  $rootScope.error = {
      'message' : (code in ERROR_MESSAGES) ? ERROR_MESSAGES[code] : ERROR_MESSAGES['our-fault'],
      'code' : code
    }
  }
  $rootScope.article = function(index) {
    return ($rootScope.json) ? $rootScope.json['articles'][index] : null;
  }
});

cApp.config(function ($routeProvider) {
  $routeProvider
    .when('/', {
      templateUrl : 'html/search.html',
      controller : 'SearchController'
    })

    .when('/results', {
      templateUrl : 'html/results.html',
      controller : 'ResultsController'
    })

    .when('/article', {
      templateUrl : 'html/read.html',
      controller : 'ReadController'
    })

    .when('/error', {
      templateUrl : 'html/error.html',
      controller : 'ErrorController'
    })
});

cApp.controller('SearchController', function($scope, $http, $rootScope, $location) {
  var SET_OPACITY = function(o) {
    $rootScope.results_style = {'opacity' : o };
  }
  $scope.is_testing = true;
  $scope.button_value = 'query';

  $scope.$watch(function() {
    return $rootScope.keyword;
  }, function() {
    var same = $rootScope.keyword.localeCompare($rootScope.last_query) != 0;
    $rootScope.can_query = same && ($rootScope.keyword.length > 0) 
    SET_OPACITY((same) ? 0.5 : 1.0);
  }, true);

  $scope.clear = function() {
    $rootScope.json = $rootScope.error = $rootScope.keyword = $rootScope.last_query = null;
    $location.path('/');
  }

  $scope.submit = function() {
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

    $http.get('/api?q=' + $rootScope.keyword + ($scope.is_testing ? '&test=1' : '')).
      success(function(res) {
        $rootScope.json = res;
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
});

cApp.controller('ResultsController', function($scope, $rootScope, $location) {
  if (!$rootScope.json) {
    $location.path('/');
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

});

cApp.controller('ReadController', function($scope) {
  console.log($scope.article);
});
