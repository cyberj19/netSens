import uuid
from collections import OrderedDict
def create(net_uuid, ts, source_uuid, target_uuid):
    return Link({
        'idx': -1,
        'uuid': 'link-%s' % uuid.uuid4().hex,
        'networkId': net_uuid,
        'firstTimeSeen': ts,
        'lastTimeSeen': ts,
        'hits': 1,
        'sourceDeviceIdx': -1,
        'targetDeviceIdx': -1,
        'sourceDeviceUUID': source_uuid,
        'targetDeviceUUID': target_uuid
    })

class Link:
    def __init__(self, dct):
        self.idx = dct['idx']
        self.uuid = dct['uuid']
        self.network_id = dct['networkId']
        self.first_time = dct['firstTimeSeen']
        self.last_time = dct['lastTimeSeen']
        self.hits = dct['hits']
        self.source_device_idx = dct['sourceDeviceIdx']
        self.target_device_idx = dct['targetDeviceIdx']
        self.source_device_uuid = dct['sourceDeviceUUID']
        self.target_device_uuid = dct['targetDeviceUUID']

    def serialize(self):
        dct = OrderedDict()
        dct['idx'] = self.idx
        dct['uuid'] = self.uuid
        dct['networkId'] = self.network_id
        dct['firstTimeSeen'] = self.first_time
        dct['lastTimeSeen'] = self.last_time
        dct['hits'] = self.hits
        dct['sourceDeviceIdx'] = self.source_device_idx
        dct['targetDeviceIdx'] = self.target_device_idx
        dct['sourceDeviceUUID'] = self.source_device_uuid
        dct['targetDeviceUUID'] = self.target_device_uuid
        return dct

    def updateDeviceMerge(self, to, fr):
        if self.source_device_uuid == fr.uuid:
            self.source_device_uuid = to.uuid
            self.source_device_idx = to.idx
        if self.target_device_uuid == fr.uuid:
            self.target_device_uuid = to.uuid
            self.target_device_idx = to.idx
    
    def matchLink(self, lnk):
        return self.source_device_uuid == lnk.source_device_uuid \
            and self.target_device_uuid == lnk.target_device_uuid

    def merge(self, lnk):
        self.hits += 1
        self.first_time = min(self.first_time, lnk.first_time)
        self.last_time = max(self.last_time, lnk.last_time)

    def match(self, arpPacket):
        if self.source_device_idx == arpPacket.source_device_idx and \
            self.target_device_idx == arpPacket.target_device_idx:
            return True
        return False

    def update(self, arpPacket):
        if arpPacket.time > self.last_time:
            self.last_time = arpPacket.time
        self.hits += 1