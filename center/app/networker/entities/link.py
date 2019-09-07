import uuid
from collections import OrderedDict
import models
class Link(models.Model):
    @classmethod
    def create(cls, net_uuid, ts, source_uuid, target_uuid):
        return Link({
            'uuid': 'link-%s' % uuid.uuid4().hex,
            'networkId': net_uuid,
            'firstTimeSeen': ts,
            'lastTimeSeen': ts,
            'sourceDeviceUUID': source_uuid,
            'targetDeviceUUID': target_uuid
        })

    def __init__(self, lnk):
        super(Link, self).__init__(schema_file='link.json', data=lnk)

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
        self.hits += lnk.hits
        self.first_time_seen = min(self.first_time_seen, lnk.first_time_seen)
        self.last_time_seen = max(self.last_time_seen, lnk.last_time_seen)

    def match(self, packet):
        try:
            if self.source_device_idx == packet.source_device_idx and \
                self.target_device_idx == packet.target_device_idx:
                return True
        finally:
            return False

    def update(self, packet):
        if packet.time > self.last_time_seen:
            self.last_time_seen = packet.time
        if packet.time < self.first_time_seen:
            self.first_time_seen = packet.time
        self.hits += 1