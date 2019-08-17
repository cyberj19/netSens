from collections import OrderedDict
from packet_aspect import PacketAspect
import models
class Packet(models.Model):
    def __init__(self, packet):
        super(Packet, self).__init__(
            schema_file='packet.json', 
            data=packet
        )

    def updateDeviceMerge(self, to, fr):
        for aspect in self.aspects:
            aspect.updateDeviceMerge(to,fr)