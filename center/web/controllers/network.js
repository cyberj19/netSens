oraApp.controller('networkController', [
    '$scope', '$rootScope',
    function ($scope, $rootScope) {
        $scope.trackIds = [-1, -1, -1];
        $scope.network = null;
        $scope.currentTab = 'devices';

        $scope.analysisId = -1;
        $scope.analysisDevice = null;

        $scope.getAnalysisData = function(id) {
            let url = $scope.apis['devAnalysis'].replace('<devId>', id);
            axios.get(url).then(
                function(response) {
                    if (!response.data.success) alert('Error getting analysis data');
                    $scope.analysisId = id;
                    $scope.analysisDevice = response.data.device;
                }
             )
        }
        $scope.setCurrentTab = function (tab) {
            if ($scope.currentTab === tab) {
                $scope.currentTab = '';
            } else {
                $scope.currentTab = tab;
            }
            // $scope.$apply();
        }
        $scope.exitNetwork = function () {
            clearInterval($scope.fetchInterval);
            console.log('unload session');
            $rootScope.$emit('exitNetwork');
        }
        $scope.clearNetwork = function() {
            $scope.trackIds = [-1, -1, -1];
            $scope.network = null;
        }

        $scope.fetch = function () {
            let url = $scope.apis['network'];
            axios.get(url).then(
                function (response) {
                    if (!response.data.success) return;
                    console.log(response.data);
                    $scope.network = response.data.network;
                    currTime = (new Date()).getTime() / 1000;
                    // $scope.session.alive = $scope.session.endTime > currTime - 10;

                    // $scope.visualize();

                    $scope.network.devices.sort((d1, d2) => {
                        return d2.lastTimeSeen - d1.lastTimeSeen;
                    });

                    $scope.network.links.sort((l1, l2) => {
                        return l2.lastTimeSeen - l1.lastTimeSeen;
                    });
                    $scope.$apply();
                }
            );
        }

        // $scope.getInterfaces = function() {
        //     axios.get('/api/interfaces').then(
        //         (resp) => {
        //             if (!resp.data.success) return;
        //             $scope.interfaces = resp.data.interfaces;
        //         }
        //     );
        // }
        
        $rootScope.$on('loadNetwork', (event, networkId) => {
            if ($scope.network && networkId !== $scope.network.id) $scope.clearNetwork();

            $scope.currentTab = 'sensors';
            $scope.apis = {
                'network': '/api/networks/' + networkId,
                'commentDevice': '/api/networks/' + networkId + '/devices/<devId>/comment',
                'closeDevice': '/api/networks/' + networkId + '/devices/<devId>/close',
                'clearNetwork': '/api/networks/' + networkId + '/clear',
                'fingerBank': '/api/networks/' + networkId + '/devices/<devId>/fingerBank',
             		'macVendors': '/api/networks/' + networkId + '/devices/<devId>/macVendors',
                // 'devAnalysis': '/api/networks/' + networkId + '/devices/<devId>/analyze'
            };
            console.log('network loaded');

            $scope.fetchInterval = setInterval(() => {
                console.log('fetching...');
                $scope.fetch();
            }, 2000);
        });

        $scope.track = function (lid, sid, tid) {
            $scope.trackIds = [lid, sid, tid];
        }
        $scope.untrack = function () {
            $scope.trackIds = [-1, -1, -1];
        }
        $scope.clearNetwork = function() {
            let url = $scope.apis['clearNetwork'];
            axios.post(url).then(function(response) {});
        }

        $scope.fingerBankAnalyze = function(devId) {
            let url = $scope.apis['fingerBank']
            url = url.replace('<devId>', devId.toString())
            axios.post(url).then(
                function(response) {
                }
            )

        }
	$scope.macVendors = function(devId) {
            let url = $scope.apis['macVendors']
            url = url.replace('<devId>', devId.toString())
            axios.post(url).then(
                function(response) {
                }
            )

        }
	$scope.isNoVendorPresent = function(vendor){
		return (vendor == null)
	}
	$scope.dhcpFpPresent = function(dhcp_fp){
		return ((dhcp_fp != null) && (dhcp_fp[0].length != 0))
	}
        $scope.closeDevice = function(devId) {
            let url = $scope.apis['closeDevice']
            url = url.replace('<devId>', devId.toString())
            axios.post(url).then(
                function(response) {
                }
            )
        }
        $scope.addComment = function (devId, currComment) {
            let url = $scope.apis['commentDevice']
            url = url.replace('<devId>', devId.toString());
            comment = prompt('Add a comment:', currComment);
            axios.post(url, {
                comment
            }).then(
                function (response) {
                }
            )
        }
        $scope.visualize = function () {
            let deviceNodes = [];
            for (let dev of $scope.devices) {
                deviceNodes.push({
                    id: dev.id + 1,
                    label: 'Dev#' + dev.id
                })
            }

            let linkEdges = [];
            for (let lnk of $scope.links) {
                linkEdges.push({
                    from: lnk.sourceDeviceId + 1,
                    to: lnk.targetDeviceId + 1
                })
            }

            let nodes = new vis.DataSet(deviceNodes);
            let edges = new vis.DataSet(linkEdges);
            let container = document.getElementById('graph');
            let network = new vis.Network(container, {
                nodes,
                edges
            }, {});
        }
        $scope.timeConverter = function (ts) {
            var a = new Date(ts * 1000);
            var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
            var year = a.getFullYear() % 2000;
            var month = a.getMonth() + 1;
            if (month < 10) month = '0' + month;
            var date = a.getDate();
            if (date < 10) date = '0' + date;

            var hour = a.getHours();
            if (hour < 10) hour = '0' + hour;

            var min = a.getMinutes();
            if (min < 10) min = '0' + min;

            var sec = a.getSeconds();
            if (sec < 10) sec = '0' + sec;

            var time = date + '/' + month + '/' + year + ' ' + hour + ':' + min + ':' + sec;
            // var time = hour + ':' + min + ':' + sec;
            return time;
        }
    }

]);