from collections import OrderedDict
import logging
import time
import uuid
import link
import device
import packet
import alert
import packet_counter
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
        'gateways': [],
        'deviceIdx': 0,
        'devices': [],
        'linkIdx': 0,
        'links': [],
        'packetIdx': 0,
        'packets': [],
        'packetCounter': {'total': 0, 'distribution': {}},
        'alertIdx': 0,
        'alerts': [],
        'targets': {}
    })

class Network:
    def __init__(self, dct):
        self.uuid = dct['uuid']
        self.name = dct['name']
        self.create_time = dct['createTime']
        self.last_update_time = dct['lastUpdateTime']
        self.gateways = dct['gateways']
        
        self.packet_counter = packet_counter.PacketCounter(dct['packetCounter'])
        
        self.device_idx = dct['deviceIdx']
        self.devices =[device.Device(dev) for dev in dct['devices']]
        
        self.link_idx = dct['linkIdx']
        self.links = [link.Link(lnk) for lnk in dct['links']]
        
        self.packet_idx = dct['packetIdx']
        self.packets = [packet.Packet(pkt) for pkt in dct['packets']]
        self.targets = dct['targets']
        
        self.alert_idx = dct['alertIdx']
        self.alerts = [alert.Alert(alrt) for alrt in dct['alerts']]
        
        self.dev_proc_queue = []
        self.lnk_proc_queue = []
        self.ip_proc_queue = []

        self.reprocess = False

    def serialize(self):
        dct = OrderedDict()
        dct['uuid'] = self.uuid
        dct['name'] = self.name
        dct['createTime'] = self.create_time
        dct['lastUpdateTime'] = self.last_update_time
        dct['gateways'] = self.gateways
        dct['deviceIdx'] = self.device_idx
        dct['devices'] = [dev.serialize() for dev in self.devices]
        dct['linkIdx'] = self.link_idx
        dct['links'] = [lnk.serialize() for lnk in self.links]
        dct['packetIdx'] = self.packet_idx
        dct['packets'] = [pkt.serialize() for pkt in self.packets]
        dct['packetCounter'] = self.packet_counter.serialize()
        dct['alertIdx'] = self.alert_idx
        dct['alerts'] = [alert.serialize() for alert in self.alerts]
        dct['targets'] = self.targets
        return dct

    def clear(self):
        self.gateways = []
        self.targets = []
        self.alerts = []
        self.packet_counter.clear()
        self.devices = []
        self.links = []
        self.packets = []

    def addPacket(self, pkt):
        pkt.network_id = self.uuid
        pkt.idx = self.packet_idx
        self.packet_idx += 1
        self.packets.append(pkt)
        self.packet_counter.add(pkt.protocol)

    def processPacket(self, pkt):
        self.addPacket(pkt)
        for aspect in pkt.aspects:
            self.processAspect(aspect, pkt.time)
    
    def processAspect(self, asp, time):
        has_source = False
        if asp.source:
            has_source = True
            sdev = device.create(self.uuid, asp.protocol, time, asp.source)
            asp.source.uuid = sdev.uuid
            self.dev_proc_queue.append(sdev)
        
        has_target = False
        if asp.target and asp.protocol != 'ip':
            has_target = True
            tdev = device.create(self.uuid, asp.protocol, time, asp.target)
            asp.target.uuid = tdev.uuid
            self.dev_proc_queue.append(tdev)
        
        if has_source and has_target:
            lnk = link.create(self.uuid, time, sdev.uuid, tdev.uuid)
            self.lnk_proc_queue.append(lnk)
        
        if asp.protocol == 'ip':
            self.ip_proc_queue.append(asp.target)

    def mergeNetwork(self, net):
        logger.debug('merging network')
        for device in net.devices:
            self.dev_proc_queue.append(device)
        for link in net.links:
            self.lnk_proc_queue.append(link)
        for mac in net.targets:
            self.mergeTarget(mac, net.targets[mac])
        self.process_queues()

    def process(self, packets):
        logger.debug('creating packet device')
        for pkt in packets:
            self.processPacket(pkt)
        
        self.process_queues()
    
    def process_queues(self):        
        logger.debug('processing device queue')
        while self.dev_proc_queue:
            nex = self.dev_proc_queue.pop(0)
            self.mergeDevice(nex)

        logger.debug('processing link queue')
        while self.lnk_proc_queue:
            nex = self.lnk_proc_queue.pop(0)
            self.mergeLink(nex)

        logger.debug('processing ip queue')
        while self.ip_proc_queue:
            nex = self.ip_proc_queue.pop(0)
            self.mergeTarget(nex.mac, [nex.ip])
        self.processTargets()

    def processTargets(self):
        self.reprocess = False
        for mac in self.targets:
            if len(self.targets[mac]) > 1:
                if mac not in self.gateways:
                    self.reprocess = True
                    self.gateways.append(mac)
                    self.addAlert('gw detected: %s' % mac)

    def mergeTarget(self, mac, ips):
        curr = self.targets.get(mac, [])
        self.targets[mac] = list(set(curr) | set(ips))

    def mergeLink(self, lnk):
        for cand_lnk in self.links:
            if cand_lnk.matchLink(lnk):
                cand_lnk.merge(lnk)
                return
        lnk.idx = self.link_idx
        self.link_idx += 1
        self.links.append(lnk)

    def mergeDevice(self, dev):
        logger.debug('[%s] matching %s', self.uuid, dev)
        bestScore = MATCH_IMPOSSIBLE
        bestMatch = None
        for cand_dev in self.devices:
            score = cand_dev.match(dev)
            logger.debug('[%s] matching to %s', self.uuid, cand_dev)
            logger.debug('[%s] score: %d', self.uuid, score)
            if score > bestScore:
                bestScore = score
                bestMatch = cand_dev

        if bestScore > MATCH_IMPOSSIBLE:
            logger.debug('[%s] found match %s', self.uuid, bestMatch)
            bestMatch.merge(dev)
            self.updateDeviceMerge(bestMatch, dev)
            if bestMatch.reprocess:
                logger.debug('[%s] reprocessing', self.uuid)
                bestMatch.reprocess = False
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
            if device.uuid != devUUID:
                continue
            for key in data:
                device.extra_data[key] = data[key]
            break

    def commentDevice(self, devUUID, comment):
        self.addDeviceData(devUUID, {'comment': comment})
    
    def addAlert(self, msg):
        alrt = alert.create(self.alert_idx, self.uuid, msg)
        self.alert_idx += 1
        self.alerts.append(alrt)