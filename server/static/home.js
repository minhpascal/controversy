var cApp = angular.module('Home', ['ngRoute', 'ngSanitize']);
var ERROR_MESSAGES = {
  'no-articles' : 'Despite our best efforts, we simply could not find any recently published English articles with that keyword. May we interest you in another try?',
  'our-fault' : 'Well, this is akward; we messed up. Please file a bug at github.com/gdyer/controversy/issues.',
  'not-logged-in' : 'A server update was just pushed! Please refresh the page and log in again.',
  'no-page' : 'Holy guacamole! We couldn\'t find that article or page (and we\'re not sure if it had anything to do with avocados or a diety).',
  'failed-to-parse' : 'There was a malformed article result that broke this response. Please try a differt keyword and file a bug at github.com/gdyer/controversy/issues.'
};

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
    return ($rootScope.json) ? $rootScope.json['articles'][index] : null;
  };
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
  .when('/results/:article/:sentence', {
    templateUrl : 'html/tweets.html',
    controller : 'TweetsController'
  })
  .when('/results/:article', {
    templateUrl : 'html/read.html',
    controller : 'ReadController'
  })
  .when('/error', {
    templateUrl : 'html/error.html',
    controller : 'ErrorController'
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
  }, true);

  $http.get('/api/stream')
    .success(function(res) {
        $scope.trending = res['top-5'];
    })
    .error(function(res) {
        $scope.trending = "< nuts, something's wrong >";
    });

  $scope.clear = function() {
    $rootScope.json = $rootScope.error = $rootScope.keyword = $rootScope.last_query = null;
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
        $rootScope.json = res;
	console.log(res);
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
    return;
  }

  $scope.readArticle = function(index) {
    $rootScope.article(index);
  }
});

cApp.controller('ErrorController', function($scope, $rootScope, $location) {
  $scope.goHome = function() {
    $location.path('/');
  };

  if (!$rootScope.error) {
    $scope.goHome();
  }
});

cApp.controller('ReadController', function($scope, $rootScope, $location, $routeParams, $window, anchorSmoothScroll) {
  $scope.articleIndex = parseInt($routeParams.article);
  if (!$scope.article || !$rootScope.json) {
    $location.path('/');
    return;
  }

  $scope.article = $rootScope.article($scope.articleIndex);
  $scope.nextExists = $scope.articleIndex < $rootScope.json['articles'].length - 1;
  $scope.previousExists = $scope.articleIndex != 0;

  $scope.change = function(i) {
    $scope.articleIndex += i;
    $location.path('read/' + $scope.articleIndex);
    $location.hash('header-content');
    anchorSmoothScroll.scrollTo('header-content');
  };

  var value = $window.innerWidth;
  $scope.lim = 150;

  if (value < 500)
  $scope.lim = 20;
  else if (value < 600)
    $scope.lim = 40;
  else if (value < 750)
    $scope.lim = 60;

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


cApp.controller('TweetsController', function($scope, $rootScope, $location, $routeParams, anchorSmoothScroll) {

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
    $location.path('read/' + $scope.articleIndex + '/' + $scope.sentenceIndex);
    $location.hash('right-header');
    anchorSmoothScroll.scrollTo('right-header');
  };

  $scope.hoverIn = function(pimg) {
    this.hovering = true;
    $scope.propic = pimg;
    $scope.globalHover = true;
  };

  $scope.hoverOut = function() {
    this.hovering = false;
    $scope.globalHover = false;
  };

});

cApp.service('anchorSmoothScroll', function(){
  this.scrollTo = function(eID) {
    var startY = currentYPosition();
    var stopY = elmYPosition(eID);
    var distance = stopY > startY ? stopY - startY : startY - stopY;
    if (distance < 100) {
      scrollTo(0, stopY);
      return;
    }
    var speed = Math.round(distance / 100);
    if (speed >= 20) speed = 20;
    var step = Math.round(distance / 25);
    var leapY = stopY > startY ? startY + step : startY - step;
    var timer = 0;
    if (stopY > startY) {
      for (var i=startY; i<stopY; i+=step) {
        setTimeout("window.scrollTo(0, "+leapY+")", timer * speed);
        leapY += step; if (leapY > stopY) leapY = stopY; timer++;
      } return;
    }
    for (var i=startY; i>stopY; i-=step) {
      setTimeout("window.scrollTo(0, "+leapY+")", timer * speed);
      leapY -= step; if (leapY < stopY) leapY = stopY; timer++;
    }

    function currentYPosition() {
      if (self.pageYOffset) return self.pageYOffset;
      if (document.documentElement && document.documentElement.scrollTop)
        return document.documentElement.scrollTop;
      if (document.body.scrollTop) return document.body.scrollTop;
      return 0;
    }

    function elmYPosition(eID) {
      var elm = document.getElementById(eID);
      var y = elm.offsetTop;
      var node = elm;
      while (node.offsetParent && node.offsetParent != document.body) {
        node = node.offsetParent;
        y += node.offsetTop;
      } return y;
    }

  };

});
