oraApp.controller(
    'overviewController',
    ['$scope', '$rootScope', function($scope, $rootScope) {
        $scope.networks = [];
        $scope.listeners = [];
        $scope.view = true;
        $scope.filterListeners = function(listeners) {
            let flisteners = [];
            for (let lstr of listeners) {
                if (lstr.agentActive)
                    flisteners.push(lstr);
            }
            return flisteners;
        }
        // $scope.getListeners = function(sensors) {
        //     let listeners = [];
        //     for (let sensor of sensors) {
        //         for (let lstr of sensor.listeners) {
        //             listeners.push({
        //                 'sensorMac': sensor.mac,
        //                 'sensorPort': sensor.port,
        //                 'interface': lstr.interface,
        //                 'lastPacketTime': lstr.lastPacketTime,
        //                 'connected': lstr.connected
        //             })
        //         }
        //     }
        //     return listeners;
        // }

        setInterval(() => {
            if (!$scope.view) return;

            axios.get('/api/overview').then(
                function(response) {
                    if (!response.data.success) return;
                    console.log(response.data);
                    $scope.networks = response.data.networks;
                    $scope.listeners = $scope.filterListeners(response.data.listeners);
                    console.log($scope.listeners);
                    $scope.$apply();
                }
            )
        }, 1000);

        $rootScope.$on('exitNetwork', (e,d) => {
            $scope.view = true;
        })
        $scope.loadNetwork = function(network) {
            console.log('Load network ', network.id);
            $rootScope.$emit('loadNetwork', network.id);
            $scope.view = false;
        };

        $scope.connectListener = function(mac, iface) {
            let url = '/api/sensors/<mac>/<iface>/connect';
            url = url.replace('<mac>', mac);
            url = url.replace('<iface>', iface)

            axios.post(url).then(
                function(response) {
                    if (!response.data.success) {
                        alert(response.data.error);
                        return;
                    }
                }
            );
        }

        
        $scope.disconnectListener = function(mac, iface) {
            let url = '/api/sensors/<mac>/<iface>/disconnect';
            url = url.replace('<mac>', mac);
            url = url.replace('<iface>', iface)

            axios.post(url).then(
                function(response) {
                    if (!response.data.success) {
                        alert(response.data.error);
                        return;
                    }
                }
            );
        }
        $scope.timeConverter = function(ts) {
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

            var time = date + ' ' + month + ' ' + year + ' ' + hour + ':' + min + ':' + sec ;
            return time;
        }
    }]
);