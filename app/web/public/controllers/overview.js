oraApp.controller(
    'overviewController',
    ['$scope', '$rootScope', '$http', function($scope, $rootScope, $http) {
        $scope.networks = [];
        $scope.listeners = [];
        $scope.view = true;

        $scope.uploadFile = function() {
            var f = document.getElementById('file').files[0];
            var fd = new FormData();
            fd.append("file", f);
            var config = { headers: { 'Content-Type': undefined },
                           transformResponse: angular.identity
                         };
            $http.post('/api/playback', fd, config).success(() => {

            });
        }
        $scope.filterListeners = function(listeners) {
            let flisteners = [];
            for (let lstr of listeners) {
                if (lstr.agentActive)
                    flisteners.push(lstr);
            }
            return flisteners;
        }

        setInterval(() => {
            if (!$scope.view) return;

            axios.get('/api/overview').then(
                function(response) {
                    if (!response.data.success) return;
                    console.log(response.data);
                    $scope.networks = response.data.networks;
                    $scope.monitor = response.data.monitor;
                    // $scope.listeners = $scope.filterListeners(response.data.listeners);
                    // console.log($scope.listeners);
                    $scope.$apply();
                }
            )
        }, 1000);

        $rootScope.$on('exitNetwork', (e,d) => {
            $scope.view = true;
        })
        $scope.loadNetwork = function(uuid) {
            console.log('Load network ', uuid);
            $rootScope.$emit('loadNetwork', uuid);
            $scope.view = false;
        };
        $scope.renameNetwork = function(uuid, name) {
            name = prompt('Choose name:', name);
            axios.post('/api/networks/'+uuid+'/rename/'+name).then(()=>{})
        }
        $scope.clearNetwork = function(uuid) {
            console.log('clear network')
            axios.post('/api/networks/' + uuid + '/clear').then(() => {})
        };
        
        $scope.removeNetwork = function(uuid) {
            console.log('remove network')
            axios.post('/api/networks/' + uuid + '/remove').then(() => {})
        };

        $scope.connectListener = function(mac, guid) {
            let url = '/api/sensors/<mac>/<guid>/connect';
            url = url.replace('<mac>', mac);
            url = url.replace('<guid>', guid)
            console.log(url);

            axios.post(url).then(
                function(response) {
                    if (!response.data.success) {
                        alert(response.data.error);
                        return;
                    }
                }
            );
        }

        
        $scope.disconnectListener = function(mac, guid) {
            let url = '/api/sensors/<mac>/<guid>/disconnect';
            url = url.replace('<mac>', mac);
            url = url.replace('<guid>', guid)

            axios.post(url).then(
                function(response) {
                    if (!response.data.success) {
                        alert(response.data.error);
                        return;
                    }
                }
            );
        }
        $scope.unixTime = function() {
            return (new Date()).getTime()/1000;
        }
        $scope.timeConverter = function(ts, short) {
            var a = new Date(ts * 1000);
            var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
            var year = a.getFullYear();
            var month = months[a.getMonth()];
            var date = a.getDate();
            if (date < 10) date = '0' + date;

            var hour = a.getHours();
            if (hour < 10) hour = '0' + hour;

            var min = a.getMinutes();
            if (min < 10) min = '0' + min;

            var sec = a.getSeconds();
            if (sec < 10) sec = '0' + sec;

            var time;
            if (short) {
                time = hour + ':' + min + ':' + sec;
            } else {
                time = date + ' ' + month + ' ' + year + ' ' + hour + ':' + min + ':' + sec ;
            }
            return time;
        }
    }]
);