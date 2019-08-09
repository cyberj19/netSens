oraApp.factory('Device', [
    function() {
        function Device(deviceData) {
            if (deviceData)
                this.setDate(deviceData);
        }

        Device.prototype = {
            setData: function(deviceData) {
                angular.extend(this, deviceData);
            },
            setComment: function(comment) {
                // TODO: post to comment url
            }
        }


    }
])