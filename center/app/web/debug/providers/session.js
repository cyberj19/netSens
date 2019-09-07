oraApp.service('sessionService', [
    'Device',
    function(Device) {
        let sessionService = {
            id: -1,
            devices: [],
            links: [],
            sensors: [],
            interfaces: [],
            _interval: null,

            _fetch: function(isOnline, sessionId) {
                let scope = this;
                let url;
                if (isOnline) {
                    url = '/api/history/sessions/' + sessionId;
                } else {
                    url = '/api/session';
                }
                axios.get(url).then(
                    function (response) {
                        if (!response.data.success) {
                            console.error('unable to load session');
                            return;
                        }
                        session = response.data.session;

                        
                        scope.id = session.id;
                        scope.devices = [];
                        for (let dev of session.devices) {
                            scope.devices.push(new Device(dev));
                        }
                        // scope.devices = session.devices;
                        scope.links = session.links;
                        scope.sensors = session.sensors;
                    }
                );

                if (isOnline) {
                    axios.get('/api/interfaces').then(
                        function(response) {
                            if (!response.data.success) {
                                console.error('unable to load interfaces');
                                return;
                            }
                            scope.interfaces = response.data.interfaces;
                        }
                    )
                }
            },
            load: function(isOnline, sessionId) {
                let scope = this;
                if (isOnline) {
                    scope._interval = setInterval(() => {
                        scope._fetch(true);
                    }, 2000);
                } else {
                    scope._fetch(false, sessionId);
                }
            },
            unload: function() {
                let scope = this;
                if (scope._interval) {
                    clearInterval(scope._interval);
                    scope._interval = null;
                }
            }
        };

        return sessionService;
    }
])