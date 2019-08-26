oraApp.controller('networkController', [
    '$scope', '$rootScope', '$http',
    function ($scope, $rootScope, $http) {
        $scope.trackIdxs = [-1, -1, -1];
        $scope.network = null;
        $scope.currentTab = 'devices';

        $scope.rename = function() {
            let name = prompt('Select name:', $scope.network.name);            
            let url = $scope.apis['renameNetwork'].replace('<name>', name);
            axios.post(url).then(() => {});
        }

        $scope.removeNetwork = function() {
            let url = $scope.apis['removeNetwork'];
            axios.post(url).then(() => {});
            $scope.exitNetwork();
        }
        $scope.analysisIdx = -1;
        $scope.analysisPackets = null;

        $scope.getAnalysisData = function(device) {
            console.log(device.uuid);
            let url = $scope.apis['devAnalysis'].replace('<devUUID>', device.uuid);
            axios.get(url).then((response)=> {
                if (!response.success) return;
                $scope.analysisIdx = device.idx;
                $scope.analysisPackets = response.packets;
            });
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
        $scope.reset = function() {
            $scope.trackIdxs = [-1, -1, -1];
            $scope.network = null;
            $scope.analysisIdx = -1;
            $scope.analysisPackets = [];
        }
        $scope.usePlugin = function(dev_uuid, plugin_uuid) {
            console.log('plugin');
            let url = $scope.apis['plugins'];
            url = url.replace('<devUUID>', dev_uuid);
            url = url.replace('<pluginUUID>', plugin_uuid);
            axios.post(url).then(()=>{});
        }
        $scope.fetch = function () {
            let url = $scope.apis['network'];
            axios.get(url).then(
                function (response) {
                    if (!response.data.success) return;
                    console.log(response.data);
                    $scope.network = response.data.network;
                    $scope.plugins = response.data.plugins;
                    currTime = (new Date()).getTime() / 1000;

                    $scope.network.devices.sort((d1, d2) => {
                        return d2.lastTimeSeen - d1.lastTimeSeen;
                    });

                    $scope.network.links.sort((l1, l2) => {
                        return l2.lastTimeSeen - l1.lastTimeSeen;
                    });
                    // $scope.buildGraph();

                    $scope.$apply();

                }
            );
        }
        $scope.addRole = function(devUUID) {
            let role = prompt('Role:');
            if (!role) return;
            let url = $scope.apis['addRoles']
                            .replace('devUUID', devUUID)
                            .replace('roles', role);
            axios.post(url).then(()=>{})
        }
        $scope.buildGraph = function() {
            let g = new sigma('graph');
            for (let dev in $scope.network.devices) {
                g.graph.addNode({
                    'id': 'd' + dev.idx,
                    'label': dev.mac || dev.hostname || dev.ip,
                })
            }

            for (let link in $scope.network.links) {
                g.graph.addEdge({
                    'id': 'l' + link.idx,
                    'label': 'link',
                    'source': 'd' + link.sourceDeviceIdx,
                    'target': 'd' + link.targetDeviceIdx
                })
            }
            g.refresh();
        }
        $rootScope.$on('loadNetwork', (event, networkId) => {
            if ($scope.network && networkId !== $scope.network.uuid) $scope.reset();

            $scope.currentTab = 'sensors';
            $scope.apis = {
                'network': '/api/networks/' + networkId,
                'commentDevice': '/api/networks/' + networkId + '/devices/<devIdx>/comment',
                'closeDevice': '/api/networks/' + networkId + '/devices/<devIdx>/close',
                'clearNetwork': '/api/networks/' + networkId + '/clear',
                'devAnalysis': '/api/networks/' + networkId + '/devices/<devUUID>/analyze',
                'renameNetwork': '/api/networks/' + networkId + '/rename/<name>',
                'removeNetwork': '/api/networks/' + networkId + '/remove',
                'plugins': '/api/networks/' + networkId + '/devices/<devUUID>/plugins/<pluginUUID>',
                'addRoles': '/api/networks/' + networkId + '/devices/<devUUID>/roles/<roles>'
            };
            console.log('network loaded');

            $scope.fetchInterval = setInterval(() => {
                console.log('fetching...');
                $scope.fetch();
            }, 2000);
        });

        $scope.track = function (lidx, sidx, tidx) {
            $scope.trackIdxs = [lidx, sidx, tidx];
        }
        $scope.untrack = function () {
            $scope.trackIdxs = [-1, -1, -1];
        }
        $scope.clearNetwork = function() {
            let url = $scope.apis['clearNetwork'];
            axios.post(url).then(function(response) {});
        }

        $scope.fingerBankAnalyze = function(devId) {
            let url = $scope.apis['fingerBank']
            url = url.replace('<devIdx>', devId.toString())
            axios.post(url).then(
                function(response) {
                }
            )

        }
	$scope.macVendors = function(devId) {
            let url = $scope.apis['macVendors']
            url = url.replace('<devIdx>', devId.toString())
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
            url = url.replace('<devIdx>', devId.toString())
            axios.post(url).then(
                function(response) {
                }
            )
        }
        $scope.addComment = function (devId, currComment) {
            let url = $scope.apis['commentDevice']
            url = url.replace('<devIdx>', devId.toString());
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
                    id: dev.idx + 1,
                    label: 'Dev#' + dev.idx
                })
            }

            let linkEdges = [];
            for (let lnk of $scope.links) {
                linkEdges.push({
                    from: lnk.sourceDeviceIdx + 1,
                    to: lnk.targetDeviceIdx + 1
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