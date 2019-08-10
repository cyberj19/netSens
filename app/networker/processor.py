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
    global network_locks
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
        net.clear()

def processPacket(packet):
    global mqtt, mongo
    logger.info('processing new packet')

def addDeviceExtraData(data):
    logger.info('add device extra data: %s', str(data))
    global mqtt, mongo
    net_uuid = data['networkUUID']
    dev_uuid = data['deviceUUID']
    ext_data = data['extraData']
    with NetworkLock(net_uuid) as net:
        net.addDeviceData(dev_uuid, ext_data)

def createTempNetwork(packets):
    global mqtt, mongo
    logger.info('Processing new packet buffer')

    net = network.create()
    packets = [packet.Packet(pkt) for pkt in packets]
    net.process(packets)
    return net

def findNetworkMatch(net):
    if net.default_gtw_mac == None:
        return None
    networks = mongo.db.networks.find({}, {'uuid': 1, 'defaultGTWMAC': 1})
    for cand_net in networks:
        if cand_net['uuid'] == net.uuid:
            continue
        if cand_net['defaultGTWMAC'] == net.default_gtw_mac:
            return cand_net
    return None

def processPacketsBuffer(packets_buffer):
    global mqtt
    origin = packets_buffer['origin']
    temp_net = createTempNetwork(packets_buffer['packets'])
    mqtt.publish('job', {'name': origin, 'progress': 70, 'finished': False})

    merge_net = findNetworkMatch(temp_net)
    if merge_net:
        with NetworkLock(merge_net['uuid']) as net:
            net.mergeNetwork(temp_net)
    else:
        mongo.addNetwork(temp_net.serialize())
    mqtt.publish('job', {'name': origin, 'progress': 100, 'finished': True})


if __name__ == '__main__':
    #inject mode
    file = sys.argv[1]
    with open(file, 'r') as fp:
        data = json.load(fp)
    net = createTempNetwork(data)