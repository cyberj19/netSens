import uuid
import packet_counter
from collections import OrderedDict
from device_match import *
import models

class Device(models.Model):
    @classmethod
    def create(cls, networkId, protocol, time, aspectDevice):
        dev = Device({
            'uuid': 'device-%s' % uuid.uuid4().hex,
            'networkId': networkId,
            'firstTimeSeen': time,
            'lastTimeSeen': time,
            'ip': aspectDevice.ip,
            'mac': aspectDevice.mac,
            'hostname': aspectDevice.hostname,
            'packetCounter': {'total': 0, 'distribution': {}},
            'extraData': aspectDevice.extra_data,
            'roles': aspectDevice.roles
        })
        dev.packet_counter.add(protocol)
        return dev

    def __init__(self, dev):
        super(Device, self).__init__(schema_file='device.json', data=dev)
        self.reprocess = False

    def __repr__(self):
        return '%d: mac=%s, ip=%s, hostname=%s' % (self.idx, self.mac, self.ip, self.hostname)

    def core(self):
        return {'ip': self.ip, 'mac': self.mac, 'hostname': self.hostname}

    def match(self, cand):
        if self.is_closed:
            return MATCH_IMPOSSIBLE
        return matchDevices(self.core(), cand.core())

    def merge(self, device):
        self.first_time_seen = min(self.first_time_seen, device.first_time_seen)
        self.last_time_seen = max(self.last_time_seen, device.last_time_seen)
        self.packet_counter.merge(device.packet_counter)
        self.extra_data.update(device.extra_data)
        self.addRoles(device.roles)
        if not self.ip and device.ip:
            self.ip = device.ip
        if not self.mac and device.mac:
            self.mac = device.mac
            self.reprocess = True
        if not self.hostname and device.hostname:
            self.hostname = device.hostname
            self.reprocess = True
    
    def addRoles(self, roles):
        self.roles = list(set(self.roles) | set(roles))

    def removeRoles(self, roles):
        self.roles = list(set(self.roles).difference(set(roles)))