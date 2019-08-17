import models

class AspectDevice(models.Model):
    def __init__(self, aspectDevice):
        super(AspectDevice, self).__init__(
            schema_file='aspect_device.json', 
            data=aspectDevice
        )

    def updateDeviceMerge(self, to, fr):
        if fr.uuid == self.uuid:
            self.idx = to.idx
            self.uuid = to.uuid