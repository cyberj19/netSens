from abc import abstractmethod
import models
class PacketAspect(models.Model):
    def __init__(self, packetAspect):
        super(PacketAspect, self).__init__(
            schema_file='packet_aspect.json', 
            data=packetAspect)

    def updateDeviceMerge(self, to, fr):
        if self.source:
            self.source.updateDeviceMerge(to, fr)
        if self.target:
            self.target.updateDeviceMerge(to, fr)