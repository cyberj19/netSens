import env
import logging
import json
import os
from business import network, packet
import sys
import threading
import contextlib
logger = logging.getLogger('proc')
mqtt = None
mongo = None

network_locks = {}
lock = threading.Lock()

@contextlib.contextmanager
def NetworkLock(uuid):
    global network_locks, lock
    global mongo
    with lock:
        if not uuid in network_locks:
            network_locks[uuid] = threading.Lock()
    with network_locks[uuid]:
        network_data = mongo.db['networks'].find_one({'uuid': uuid})
        if not network_data:
            net = None
        else:
            net = network.Network(network_data)
        yield net
        if net:
            mongo.saveNetwork(net.serialize())


def renameNetwork(data):
    logger.info('request to change network name')
    uuid = data['uuid']
    name = data['name']
    with NetworkLock(uuid) as net:
        if net:
            net.name = name

def removeNetwork(data):
    uuid = data['uuid']
    with NetworkLock(uuid):
        mongo.deleteNetwork(uuid)

def clearNetwork(data):
    uuid = data['uuid']
    with NetworkLock(uuid) as net:
        if net:
            net.clear()

def addDeviceExtraData(data):
    logger.info('add device extra data: %s', str(data))
    global mqtt, mongo
    net_uuid = data['networkUUID']
    dev_uuid = data['deviceUUID']
    ext_data = data['extraData']
    with NetworkLock(net_uuid) as net:
        if net:
            net.addDeviceData(dev_uuid, ext_data)

def findNetworkMatch(net):
    if not net.gateways:
        return None
    networks = mongo.db.networks.find({}, {'uuid': 1, 'gateways': 1})
    for cand_net in networks:
        if cand_net['uuid'] == net.uuid:
            continue
        cand_gtw = cand_net['gateways']
        if not set(cand_gtw).isdisjoint(set(net.gateways)):
            return cand_net['uuid']
    return None

def getNetworkForOrigin(org_uuid):
    pairs = mongo.db.origins.find({})
    for pair in pairs:
        if pair['originUUID'] == org_uuid:
            return pair['networkUUID']
    return None

def addOriginNetwork(net_uuid, org_uuid):
    mongo.db.origins.insert_one({
        'originUUID': org_uuid, 
        'networkUUID': net_uuid
        })

def updateOriginNetwork(old_net_uuid, new_net_uuid):
    mongo.db.origins.update({
            'networkUUID': old_net_uuid
        }, {
            '$set': {'networkUUID': new_net_uuid}
        },
        upsert=False)
def processPacketsBuffer(packets_buffer):
    logger.info('Processing new packet buffer')
    network_queue = []
    org_uuid = packets_buffer['origin']
    packets = [packet.Packet(pkt) for pkt in packets_buffer['packets']]
    
    dest_uuid = getNetworkForOrigin(org_uuid)
    if not dest_uuid:
        net = network.create()
        dest_uuid = net.uuid
        mongo.addNetwork(net.serialize())
        addOriginNetwork(dest_uuid, org_uuid)
    with NetworkLock(dest_uuid) as net:
        net.process(packets)
        if net.reprocess:
            network_queue.append(net)
            net.reprocess = False
    altered_networks = processNetworkQueue(network_queue)
    for uuid in altered_networks:
        network_data = mongo.db.networks.find_one({'uuid': uuid})
        if network_data:
            for device in network_data['devices']:
                mqtt.publish('device', device)

def processNetworkQueue(network_queue):
    altered_networks = [network_queue[0].uuid]
    while network_queue:
        nex = network_queue.pop(0)
        with NetworkLock(nex.uuid):
            merge_uuid = findNetworkMatch(nex)
            if merge_uuid:
                with NetworkLock(merge_uuid) as merge_net:
                    merge_net.mergeNetwork(nex)
                    altered_networks.append(merge_uuid)
                    altered_networks.remove(nex.uuid)
                    mongo.deleteNetwork(nex.uuid)
                    updateOriginNetwork(nex.uuid, merge_uuid)
                    if merge_net.reprocess:
                        network_queue.append(merge_net)
                        merge_net.reprocess = False
    return altered_networks