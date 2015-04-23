angular.module('Home', [])
.config(function ($routeProvider) {
  $routeProvider
    .when('/', {
      templateUrl : ''
    })
});
.controller('KeywordController', function($scope, $http) {
  var SET_OPACITY = function(o) {
    $scope.results_style = {'opacity' : o };
  }
  var LAST_QUERY = '';
  var messages = {
    'no-articles' : 'Despite our best efforts, we simply could not find any articles with that keyword. May we interest you in another try?',
    'our-fault' : 'Well, this is akward; we messed up. Please file a bug at github.com/gdyer/controversy/issues.',
    'not-logged-in' : 'A server update was just pushed! Please refresh the page and log in again.'
  };


  $scope.is_testing = true;
  $scope.button_value = 'query';
  $scope.keyword = '';
  $scope.$watch('keyword', function() {
    $scope.can_query = $scope.keyword.length > 0;
    if ($scope.keyword.localeCompare(LAST_QUERY) != 0)
    SET_OPACITY(.5);
    else {
      SET_OPACITY(1);
      $scope.can_query = false;
    }

  });

  $scope.clear = function() {
    $scope.json = null;
    $scope.error_message = null;
    LAST_QUERY = '';
  }

  $scope.submit = function() {
    /* 
     * for now, just show unranked content...
     */

    if ($scope.is_loading || !$scope.can_query)
      return;

    $scope.error_message = null;
    LAST_QUERY = $scope.keyword; 
    $scope.button_value = 'querying...';
    $scope.is_loading = true;

    $http.get('/api?q=' + $scope.keyword + ($scope.is_testing ? '&test=1' : '')).
      success(function(res) {
        $scope.json = res;
        if (res['error']) {
          $scope.error_img = res['message'];
          $scope.error_message = messages[$scope.error_img];
        }
        $scope.can_query = $scope.is_loading = false;
        $scope.button_value = 'query';
        SET_OPACITY(1.0);

      }).
    error(function(res) {
      $scope.error_img = 'our-fault';
      $scope.error_message = messages[$scope.error_img];
      $scope.is_loading = false;
      $scope.json = {};
      $scope.button_value = 'problems...';
    });
  };
});
