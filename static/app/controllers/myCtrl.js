app.controller('myCtrl', function($scope) {
    $scope.firstName= "John";
    $scope.lastName= "Doe";
});

app.controller('bgchange', function($scope, $timeout) {
	$scope.bg='http://grofers.com/blog/wp-content/uploads/2016/01/banner_4.jpg';
	$timeout(function () {
      $scope.bg = 'http://grofers.com/blog/wp-content/uploads/2016/01/banner_1.jpg';
  }, 2000);
});

app.controller('http', function($scope, $http, $interval) {

	$scope.theTime = new Date().toLocaleTimeString();
	var myDiv = document.getElementById("output");

    $interval(function () {
        $http.get("/chat").then(function (response) {
        	$scope.myData = response.data.message;
        	myDiv.scrollTop = myDiv.scrollHeight;
    });
    }, 1000);

	$scope.send1 = function()
	{
		$scope.theTime = new Date().toLocaleTimeString();
		$http.post('/chat', {'payload' : {'message' : $scope.input1 , 'time' : $scope.theTime} });
	}
});