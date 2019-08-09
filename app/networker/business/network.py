from collections import OrderedDict
import logging
import vendors
import time
import uuid
import link
import device
import packet
from device import MATCH_CERTAIN, MATCH_IMPOSSIBLE, MATCH_POSSIBLE
logger = logging.getLogger('network')

def create():
    tt = time.time()
    uid = 'net-%s' % uuid.uuid4().hex
    return Network({
        'uuid': uid,
        'name': uid,
        'createTime': tt,
        'lastUpdateTime': tt,
        'defaultGTWMAC': None,
        'defaultGTWIP': None,
        'deviceIdx': 0,
        'devices': [],
        'linkIdx': 0,
        'links': [],
        'packetIdx': 0,
        'packets': []
    })

class Network:
    def __init__(self, dct):
        logger.debug(dct)
        self.uuid = dct['uuid']
        self.name = dct['name']
        self.create_time = dct['createTime']
        self.last_update_time = dct['lastUpdateTime']
        self.default_gtw_mac = dct['defaultGTWMAC']
        self.default_gtw_ip = dct['defaultGTWIP']
        self.device_idx = dct['deviceIdx']
        self.devices =[device.Device(dev) for dev in dct['devices']]
        self.link_idx = dct['linkIdx']
        self.links = [link.Link(lnk) for lnk in dct['links']]
        self.packet_idx = dct['packetIdx']
        self.packets = [packet.parsePacket(pkt) for pkt in dct['packets']]

        self.dev_proc_queue = []
        self.lnk_proc_queue = []

    def serialize(self):
        dct = OrderedDict()
        dct['uuid'] = self.uuid
        dct['name'] = self.name
        dct['createTime'] = self.create_time
        dct['lastUpdateTime'] = self.last_update_time
        dct['defaultGTWMAC'] = self.default_gtw_mac
        dct['defaultGTWIP'] = self.default_gtw_ip
        dct['deviceIdx'] = self.device_idx
        dct['devices'] = [dev.serialize() for dev in self.devices]
        dct['linkIdx'] = self.link_idx
        dct['links'] = [lnk.serialize() for lnk in self.links]
        dct['packetIdx'] = self.packet_idx
        dct['packets'] = [pkt.serialize() for pkt in self.packets]
        return dct

    def createPacketDevice(self, pkt):
        pkt.network_id = self.uuid
        pkt.idx = self.packet_idx
        self.packet_idx += 1
        self.packets.append(pkt)
        if pkt.type == 'arp':
            sdev = device.create(self.uuid, pkt.time, pkt.source_device_ip, 
                                pkt.source_device_mac)
            sdev.hits = 1
            sdev.arp_hits = 1
            pkt.source_device_uuid = sdev.uuid
            
            tdev = device.create(self.uuid, pkt.time, pkt.target_device_ip)
            tdev.hits = 1
            tdev.arp_hits = 1
            pkt.target_device_uuid = tdev.uuid

            lnk = link.create(self.uuid, pkt.time, sdev.uuid, tdev.uuid)
            self.dev_proc_queue.append(sdev)
            self.dev_proc_queue.append(tdev)
            self.lnk_proc_queue.append(lnk)
        elif pkt.type == 'dhcp':
            sdev = device.create(self.uuid, pkt.time, 
                                ip=None, mac=pkt.source_device_mac,
                                dhcp_fp=pkt.dhcp_fp)
            sdev.hits = 1
            sdev.dhcp_hits = 1
            pkt.source_device_uuid = sdev.uuid
            self.dev_proc_queue.append(sdev)
    
    def process(self, packets):
        logger.debug('creating packet device')
        for pkt in packets:
            self.createPacketDevice(pkt)
        logger.debug('processing device queue')
        while self.dev_proc_queue:
            nex = self.dev_proc_queue.pop(0)
            self.mergeDevice(nex)
        logger.debug('processing link queue')
        while self.lnk_proc_queue:
            nex = self.lnk_proc_queue.pop(0)
            self.mergeLink(nex)
    
    def mergeLink(self, lnk):
        for cand_lnk in self.links:
            if cand_lnk.matchLink(lnk):
                cand_lnk.merge(lnk)
                return
        lnk.idx = self.link_idx
        self.link_idx += 1
        self.links.append(lnk)

    def mergeDevice(self, dev):
        logger.debug('[%s] merging %s', self.uuid, dev.uuid)
        bestScore = MATCH_IMPOSSIBLE
        bestMatch = None
        for cand_dev in self.devices:
            score = cand_dev.match(dev.first_time, cand_ip=dev.ip, cand_mac=dev.mac)
            logger.debug('[%s] matching to %s: %d', self.uuid, cand_dev.uuid, score)
            if score > bestScore:
                bestScore = score
                bestMatch = cand_dev

        if bestScore > MATCH_IMPOSSIBLE:
            logger.debug('[%s] found match %d', self.uuid, bestMatch.idx)
            reprocess = bestMatch.merge(dev)
            self.updateDeviceMerge(bestMatch, dev)
            if reprocess:
                logger.debug('[%s] reprocessing', self.uuid)
                self.dev_proc_queue.insert(0, bestMatch)
        else:
            dev.idx = self.device_idx
            self.device_idx += 1
            self.devices.append(dev)
            self.updateDeviceMerge(dev, dev)
            logger.debug('[%s] no match found. creating new device with idx %d', self.uuid, dev.idx)

    def updateDeviceMerge(self, to, fr):
        for lnk in self.links:
            lnk.updateDeviceMerge(to, fr)
        for lnk in self.lnk_proc_queue:
            lnk.updateDeviceMerge(to, fr)
        for pkt in self.packets:
            pkt.updateDeviceMerge(to, fr)

    def addDeviceData(self, devUUID, data):
        for device in self.devices:
            if device.uuid != self.devices[devUUID]:
                continue
            temp = dict(device.extra_data)
            temp.update(data)
            device.extra_data = temp
            break

    def commentDevice(self, devUUID, comment):
        self.addDeviceData(devUUID, {'comment': comment})
