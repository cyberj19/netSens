from collections import OrderedDict
from packet_aspect import PacketAspect

class Packet(object):
    def __init__(self, packet):
        self.idx = packet.get('idx', None)
        self.uuid = packet['uuid']
        self.time = packet['time']
        self.origin = packet['origin']
        self.network_id = packet.get('networkId', None)
        self.protocol = packet['protocol']
        self.layer = packet['layer']
        self.aspects = [PacketAspect(aspect) for aspect in packet['aspects']]        
    
    def serialize(self):
        packet = OrderedDict()
        packet['idx'] = self.idx
        packet['uuid'] = self.uuid
        packet['time'] = self.time
        packet['origin'] = self.origin
        packet['networkId'] = self.network_id
        packet['protocol'] = self.protocol
        packet['layer'] = self.layer
        packet['aspects'] = [aspect.serialize() for aspect in self.aspects]
        return packet

    def updateDeviceMerge(self, to, fr):
        for aspect in self.aspects:
            aspect.updateDeviceMerge(to,fr)