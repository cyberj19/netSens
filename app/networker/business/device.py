import vendors
import uuid
import packet_counter
from collections import OrderedDict
MATCH_IMPOSSIBLE = 0
MATCH_POSSIBLE = 1
MATCH_CERTAIN = 2

def create(net_uuid, pktType, ts, ip=None, mac=None, dhcp_fp=None):
    if mac:
        vendor = vendors.getVendor(mac)
    else:
        vendor = None
    dev = Device({
        'idx': -1,
        'uuid': 'device-%s' % uuid.uuid4().hex,
        'isClosed': False,
        'networkId': net_uuid,
        'firstTimeSeen': ts,
        'lastTimeSeen': ts,
        'ip': ip,
        'mac': mac,
        'vendor': vendor,
        'packetCounter': {'total': 0, 'distribution': {}},
        'dhcpFingerPrint': dhcp_fp
    })
    dev.packet_counter.add(pktType)
    return dev
class Device:
    def __init__(self, dct):
        if not 'extraData' in dct:
            dct['extraData'] = {}
        if not 'dhcpFingerPrint' in dct:
            dct['dhcpFingerPrint'] = None

        self.idx = dct['idx']
        self.uuid = dct['uuid']
        self.is_closed = dct['isClosed']
        self.network_id = dct['networkId']
        self.first_time = dct['firstTimeSeen']
        self.last_time = dct['lastTimeSeen']
        self.ip = dct['ip']
        self.mac = dct['mac']
        self.vendor = dct['vendor']
        self.packet_counter = packet_counter.PacketCounter(dct['packetCounter'])
        self.extra_data = dct['extraData']
        self.dhcp_fp = dct['dhcpFingerPrint']
        if self.dhcp_fp:
            self.extra_data.update({"VCI": self.dhcp_fp[1], "Hostname": self.dhcp_fp[2]})

        self.reprocess = False
        
    def addPacket(self, packetType, time, ip=None, mac=None, dhcp_fp=None):
        self.packet_counter.add(packetType)
        if time > self.last_time:
            self.last_time = time
        
        self.reprocess = False
        if mac:
            if not self.mac:
                self.reprocess = True
            vendor = vendors.getVendor(mac)
            self.mac = mac
            self.vendor = vendor
        
        if ip:
            self.ip = ip
        
        if dhcp_fp:
            self.dhcp_fp = dhcp_fp
            temp = dict(self.extra_data)
            temp.update({'VCI': dhcp_fp[1], 'Hostname': dhcp_fp[2]})
            self.extra_data = temp

    def match(self, time, cand_ip=None, cand_mac=None):
        if self.is_closed:
            return MATCH_IMPOSSIBLE
        if not cand_ip and not cand_mac: # nothing is known about candidate
            return MATCH_IMPOSSIBLE
        elif cand_ip: # only candidate ip is known
            # TODO: add time test
            if self.ip and self.ip == cand_ip:
                return MATCH_POSSIBLE
            else:
                return MATCH_IMPOSSIBLE
        elif cand_mac: # only candidate mac is known
            if self.mac:
                if self.mac == cand_mac:
                    return MATCH_CERTAIN
                else:
                    return MATCH_IMPOSSIBLE
            else:
                return MATCH_IMPOSSIBLE
        else: # ip and mac are known
            if self.mac:
                if self.mac == cand_mac:
                    return MATCH_CERTAIN
                else:
                    return MATCH_IMPOSSIBLE
            elif self.ip:
                if self.ip == cand_ip:
                    return MATCH_POSSIBLE
                else:
                    return MATCH_IMPOSSIBLE

    def merge(self, device):
        self.first_time = min(self.first_time, device.first_time)
        self.last_time = max(self.last_time, device.last_time)
        self.packet_counter.merge(device.packet_counter)
        self.extra_data.update(device.extra_data)
        if not self.ip and device.ip:
            self.ip = device.ip

    def serialize(self):
        dct = OrderedDict()
        dct['idx'] = self.idx
        dct['uuid'] = self.uuid
        dct['networkId'] = self.network_id
        dct['isClosed'] = self.is_closed
        dct['firstTimeSeen'] = self.first_time
        dct['lastTimeSeen'] = self.last_time
        dct['ip'] = self.ip
        dct['mac'] = self.mac
        dct['vendor'] = self.vendor
        dct['packetCounter'] = self.packet_counter.serialize()
        dct['extraData'] = self.extra_data
        dct['dhcpFingerPrint'] = self.dhcp_fp
        return dct