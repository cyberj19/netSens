from collections import OrderedDict
from abc import abstractmethod
class Packet(object):
    def __init__(self, dct):
        if not 'networkId' in dct:
            dct['networkId'] = None
        if not 'idx' in dct:
            dct['idx'] = None

        self.idx = dct['idx']
        self.uuid = dct['uuid']
        self.time = dct['time']
        self.type = dct['type']
        self.origin = dct['origin']
        self.network_id = dct['networkId']
        
    def serialize(self):
        dct = OrderedDict()
        dct['idx'] = self.idx
        dct['uuid'] = self.uuid
        dct['time'] = self.time
        dct['type'] = self.type
        dct['origin'] = self.origin
        dct['networkId'] = self.network_id
        return dct

    @abstractmethod
    def updateDeviceMerge(self, to, fr):
        pass
class ARPPacket(Packet):
    def __init__(self, dct):
        super(ARPPacket, self).__init__(dct)
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
        dct = super(ARPPacket, self).serialize()
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

class DHCPPacket(Packet):
    def __init__(self, dct):
        super(DHCPPacket, self).__init__(dct)
        if not 'sourceDeviceIdx' in dct:
            dct['sourceDeviceIdx'] = None
        if not 'sourceDeviceUUID' in dct:
            dct['sourceDeviceUUID'] = None
        self.source_device_uuid = dct['sourceDeviceUUID']
        self.source_device_idx = dct['sourceDeviceIdx']
        self.source_device_mac = dct['sourceDeviceMAC']
        self.dhcp_fp = dct['dhcpFingerPrint']

    def serialize(self):
        dct = super(DHCPPacket, self).serialize()
        dct['sourceDeviceUUID'] = self.source_device_uuid
        dct['sourceDeviceIdx'] = self.source_device_idx
        dct['sourceDeviceMAC'] = self.source_device_mac
        dct['dhcpFingerPrint'] = self.dhcp_fp
        return dct

    def updateDeviceMerge(self, to, fr):
        if self.source_device_uuid == fr.uuid:
            self.source_device_idx = to.idx
            self.source_device_uuid = to.uuid

def parsePacket(dct):
    if dct['type'] == 'arp':
        return ARPPacket(dct)
    elif dct['type'] == 'dhcp':
        return DHCPPacket(dct)
    else:
        raise Exception('Unknown packet type %s' % dct['type'])