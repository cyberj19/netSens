from collections import OrderedDict
import packet_aspect

class Packet(object):
    def __init__(self, dct):
        if not 'idx' in dct:
            dct['idx'] = None
        if not 'networkId' in dct:
            dct['networkId'] = None
        self.idx = dct['idx']
        self.uuid = dct['uuid']
        self.time = dct['time']
        self.origin = dct['origin']
        self.network_id = dct['networkId']
        self.protocol = dct['protocol']
        self.aspects = [packet_aspect.parse(aspect) for aspect in dct['aspects']]        
    
    def serialize(self):
        dct = OrderedDict()
        dct['idx'] = self.idx
        dct['uuid'] = self.uuid
        dct['time'] = self.time
        dct['origin'] = self.origin
        dct['networkId'] = self.network_id
        dct['protocol'] = self.protocol
        dct['aspects'] = [aspect.serialize() for aspect in self.aspects]
        return dct

    def updateDeviceMerge(self, to, fr):
        for aspect in self.aspects:
            aspect.updateDeviceMerge(to,fr)