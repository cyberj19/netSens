from collections import OrderedDict
from abc import abstractmethod
class PacketAspect(object):
    def __init__(self, packetAspect):
        self.protocol = packetAspect['protocol']
        self.layer = packetAspect['layer']
    
    def serialize(self):
        packetAspect = OrderedDict()
        packetAspect['protocol'] = self.protocol
        packetAspect['layer'] = self.layer
        return packetAspect
    
    @abstractmethod
    def updateDeviceMerge(self, to, fr):
        pass

class ARPAspect(PacketAspect):
    def __init__(self, dct):
        super(ARPAspect, self).__init__(dct)
        if not 'sourceDeviceIdx' in dct:
            dct['sourceDeviceIdx'] = None
        if not 'targetDeviceIdx' in dct:
            dct['targetDeviceIdx'] = None
        if not 'sourceDeviceUUID' in dct:
            dct['sourceDeviceUUID'] = None
        if not 'targetDeviceUUID' in dct:
            dct['targetDeviceUUID'] = None
        
        self.source_device_uuid = dct['sourceDeviceUUID']
        self.source_device_idx = dct['sourceDeviceIdx']
        self.source_device_ip = dct['sourceDeviceIP']
        self.source_device_mac = dct['sourceDeviceMAC']
        self.target_device_uuid = dct['targetDeviceUUID']
        self.target_device_idx = dct['targetDeviceIdx']
        self.target_device_ip = dct['targetDeviceIP']

    def serialize(self):
        dct = super(ARPAspect, self).serialize()
        dct['sourceDeviceUUID'] = self.source_device_uuid
        dct['sourceDeviceIdx'] = self.source_device_idx
        dct['sourceDeviceIP'] = self.source_device_ip
        dct['sourceDeviceMAC'] = self.source_device_mac
        dct['targetDeviceUUID'] = self.target_device_uuid
        dct['targetDeviceIdx'] = self.target_device_idx
        dct['targetDeviceIP'] = self.target_device_ip
        return dct
    
    def updateDeviceMerge(self, to, fr):
        if self.source_device_uuid == fr.uuid:
            self.source_device_uuid = to.uuid
            self.source_device_idx = to.idx
        if self.target_device_uuid == fr.uuid:
            self.target_device_uuid = to.uuid
            self.target_device_idx = to.idx

class IPAspect(PacketAspect):
    def __init__(self, dct):
        super(IPAspect, self).__init__(dct)
        self.target_device_ip = dct['targetDeviceIP']
        self.target_device_mac = dct['targetDeviceMAC']
    
    def serialize(self):
        dct = super(IPAspect, self).serialize()
        dct['targetDeviceMAC'] = self.target_device_mac
        dct['targetDeviceIP'] = self.target_device_ip
        return dct
    
class DHCPAspect(PacketAspect):
    def __init__(self, dct):
        super(DHCPAspect, self).__init__(dct)
        if not 'sourceDeviceIdx' in dct:
            dct['sourceDeviceIdx'] = None
        if not 'sourceDeviceUUID' in dct:
            dct['sourceDeviceUUID'] = None
        self.source_device_uuid = dct['sourceDeviceUUID']
        self.source_device_idx = dct['sourceDeviceIdx']
        self.source_device_mac = dct['sourceDeviceMAC']
        self.dhcp_fp = dct['dhcpFingerPrint']

    def serialize(self):
        dct = super(DHCPAspect, self).serialize()
        dct['sourceDeviceUUID'] = self.source_device_uuid
        dct['sourceDeviceIdx'] = self.source_device_idx
        dct['sourceDeviceMAC'] = self.source_device_mac
        dct['dhcpFingerPrint'] = self.dhcp_fp
        return dct

    def updateDeviceMerge(self, to, fr):
        if self.source_device_uuid == fr.uuid:
            self.source_device_idx = to.idx
            self.source_device_uuid = to.uuid

def parse(dct):
    if dct['protocol'] == 'arp':
        return ARPAspect(dct)
    elif dct['protocol'] == 'dhcp':
        return DHCPAspect(dct)
    elif dct['protocol'] == 'ip':
        return IPAspect(dct)
    else:
        raise Exception('Unknown packet type %s' % dct['type'])