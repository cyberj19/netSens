from collections import OrderedDict
from abc import abstractmethod
class PacketAspect(object):
    def __init__(self, packetAspect):
        self.protocol = packetAspect['protocol']
        self.layer = packetAspect['layer']
        self.time = packetAspect['time']
        self.description = packetAspect['description']
        if 'source' in packetAspect:
            self.source = AspectDevice(packetAspect['source'])
        else:
            self.source = None
        
        if 'target' in packetAspect:
            self.target = AspectDevice(packetAspect['target'])
        else:
            self.target = None

    def serialize(self):
        packetAspect = OrderedDict()
        packetAspect['protocol'] = self.protocol
        packetAspect['layer'] = self.layer
        packetAspect['time'] = self.time
        packetAspect['description'] = self.description
        if self.source:
            packetAspect['source'] = self.source.serialize()
        if self.target:
            packetAspect['target'] = self.target.serialize()
        return packetAspect

    def updateDeviceMerge(self, to, fr):
        if self.source:
            self.source.updateDeviceMerge(to, fr)
        if self.target:
            self.target.updateDeviceMerge(to, fr)
    
class AspectDevice:
    def __init__(self, aspectDevice):
        self.uuid = aspectDevice.get('uuid', None)
        self.idx = aspectDevice.get('idx', None)
        self.ip = aspectDevice.get('ip', None)
        self.mac = aspectDevice.get('mac', None)
        self.hostname = aspectDevice.get('hostname', None)
        self.extra_data = aspectDevice.get('extraData', {})
    
    def serialize(self):
        aspectDevice = OrderedDict()
        aspectDevice['uuid'] = self.uuid
        aspectDevice['idx'] = self.idx
        aspectDevice['ip'] = self.ip
        aspectDevice['mac'] = self.mac
        aspectDevice['hostname'] = self.hostname
        aspectDevice['extraData'] = self.extra_data
        return aspectDevice

    def updateDeviceMerge(self, to, fr):
        if fr.uuid == self.uuid:
            self.idx = to.idx
            self.uuid = to.uuid