import uuid
import packet_counter
from collections import OrderedDict
MATCH_IMPOSSIBLE = 0
MATCH_POSSIBLE = 1
MATCH_CERTAIN = 2

match_rules = [
    {
        'properties': ['mac'],
        'score': MATCH_CERTAIN
    },
    {
        'properties': ['ip', 'hostname'],
        'score': MATCH_CERTAIN
    },
    {
        'properties': ['ip'],
        'score': MATCH_POSSIBLE
    },
    {
        'properties': ['hostname'],
        'score': MATCH_POSSIBLE
    }
]
def create(networkId, protocol, time, aspectDevice):
    dev = Device({
        'idx': -1,
        'uuid': 'device-%s' % uuid.uuid4().hex,
        'isClosed': False,
        'networkId': networkId,
        'firstTimeSeen': time,
        'lastTimeSeen': time,
        'ip': aspectDevice.ip,
        'mac': aspectDevice.mac,
        'hostname': aspectDevice.hostname,
        'packetCounter': {'total': 0, 'distribution': {}},
        'extraData': aspectDevice.extra_data
    })
    dev.packet_counter.add(protocol)
    return dev
class Device:
    def __init__(self, dct):
        self.idx = dct['idx']
        self.uuid = dct['uuid']
        self.is_closed = dct['isClosed']
        self.network_id = dct['networkId']
        self.first_time_seen = dct['firstTimeSeen']
        self.last_time_seen = dct['lastTimeSeen']
        self.ip = dct['ip']
        self.mac = dct['mac']
        self.hostname = dct['hostname']
        self.packet_counter = packet_counter.PacketCounter(dct['packetCounter'])
        self.extra_data = dct.get('extraData', {})
        self.core = {'ip': self.ip, 'mac': self.mac, 'hostname': self.hostname}
        self.reprocess = False
    def __repr__(self):
        return '%d: mac=%s, ip=%s, hostname=%s' % (self.idx, self.mac, self.ip, self.hostname)
    
    def match(self, cand):
        if self.is_closed:
            return MATCH_IMPOSSIBLE

        matches = []
        for prop in ['mac', 'ip', 'hostname']:
            my = self.core[prop]
            other = cand.core[prop]
            if other:
                if other == my:
                    matches.append(prop)
                else:
                    matches.append('!' + prop)
        
        best_score = MATCH_IMPOSSIBLE
        for rule in match_rules:
            if set(rule['properties']).issubset(set(matches)):
                if rule['score'] > best_score:
                    best_score = rule['score']
        return best_score

    def merge(self, device):
        self.first_time_seen = min(self.first_time_seen, device.first_time_seen)
        self.last_time_seen = max(self.last_time_seen, device.last_time_seen)
        self.packet_counter.merge(device.packet_counter)
        self.extra_data.update(device.extra_data)
        if not self.ip and device.ip:
            self.ip = device.ip
        if not self.mac and device.mac:
            self.mac = device.mac
            self.reprocess = True
        if not self.hostname and device.hostname:
            self.hostname = device.hostname
            self.reprocess = True

    def serialize(self):
        dct = OrderedDict()
        dct['idx'] = self.idx
        dct['uuid'] = self.uuid
        dct['networkId'] = self.network_id
        dct['isClosed'] = self.is_closed
        dct['firstTimeSeen'] = self.first_time_seen
        dct['lastTimeSeen'] = self.last_time_seen
        dct['ip'] = self.ip
        dct['mac'] = self.mac
        dct['hostname'] = self.hostname
        dct['packetCounter'] = self.packet_counter.serialize()
        dct['extraData'] = self.extra_data
        return dct