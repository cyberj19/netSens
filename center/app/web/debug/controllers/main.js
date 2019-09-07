oraApp.controller('mainController',[
    '$scope','$rootScope',
    function($scope, $rootScope) {
        $scope.overview = true;


        $rootScope.$on('loadNetwork', () => {
            $scope.overview = false;
        });
        $rootScope.$on('exitNetwork', ()=> {
            $scope.overview = true;
        });

    }
])