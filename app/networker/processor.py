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
    with lock:
        if not uuid in network_locks:
            network_locks[uuid] = threading.Lock()
    network_locks[uuid].acquire(True)
    yield network_locks[uuid]
    network_locks[uuid].release()

def renameNetwork(data):
    uuid = data['uuid']
    name = data['name']
    with NetworkLock(uuid):
        mongo.db['networks'].update_one({'uuid': uuid}, {'$set': {'name': name}}, upsert=False)

def removeNetwork(data):
    uuid = data['uuid']
    with NetworkLock(uuid):
        mongo.db['networks'].delete_one({'uuid': uuid})
        # mongo.db['packets'].delete({'networkId': uuid})

def clearNetwork(data):
    uuid = data['uuid']
    with NetworkLock(uuid):
        mongo.db['networks'].update_one(
            {'uuid': uuid},
            {
                '$set': {
                    'devices': [],
                    'links': [],
                    'packets': []
                }
            },
            upsert=False
        )

def processPacket(packet):
    global mqtt, mongo
    logger.info('processing new packet')
    
def processPacketsBuffer(packets_buffer):
    global mqtt, mongo
    logger.info('Processing new packet buffer')

    net = None
    if 'destNetwork' in packets_buffer and mongo:
        uuid = packets_buffer['destNetwork']
        network_data = mongo.db['networks'].find_one({'uuid': uuid})
        if network_data:
            net = network.Network(network_data)
            mode = 'update'
    if not net:
        net = network.create()
        mode = 'new'
    packets = [packet.parsePacket(pkt) for pkt in packets_buffer['packets']]
    net.process(packets)
    net_data = net.serialize()
    net_file = os.path.join(env.output_folder, '%s.json' % net.uuid)
    with open(net_file, 'w') as f:
        json.dump(net_data, f, indent=4)
        
    if mongo:
        with NetworkLock(net.uuid):
            mongo.db['networks'].update_one(
                {'uuid': net.uuid},
                {'$set': net_data},
                upsert=(mode=='new'))
        # mongo.db['packets'].insert_many(packets_data)

if __name__ == '__main__':
    #inject mode
    file = sys.argv[1]
    with open(file, 'r') as fp:
        data = json.load(fp)
    processPacketsBuffer(data)