name = 'packets_buffer'
topic = 'packetsBuffer'
from entities.network import Network
from entities.packet import Packet

NetworkLock = None
logger = None
db_client = None
mq_client = None

def init(mq, db, nlock, lgr):
    global NetworkLock, logger, db_client, mq_client
    mq_client = mq
    db_client = db
    NetworkLock = nlock
    logger = lgr

def findNetworkMatch(net):
    if not net.gateways:
        return None
    networks = db_client.db.networks.find({}, {'uuid': 1, 'gateways': 1})
    for cand_net in networks:
        if cand_net['uuid'] == net.uuid:
            continue
        cand_gtw = cand_net['gateways']
        if not set(cand_gtw).isdisjoint(set(net.gateways)):
            return cand_net['uuid']
    return None

def getNetworkForOrigin(org_uuid):
    pairs = db_client.db.origins.find({})
    for pair in pairs:
        if pair['originUUID'] == org_uuid:
            return pair['networkUUID']
    return None

def addOriginNetwork(net_uuid, org_uuid):
    db_client.db.origins.insert_one({
        'originUUID': org_uuid, 
        'networkUUID': net_uuid
        })

def updateOriginNetwork(old_net_uuid, new_net_uuid):
    db_client.db.origins.update({
            'networkUUID': old_net_uuid
        }, {
            '$set': {'networkUUID': new_net_uuid}
        },
        upsert=False)

def process(packets_buffer):
    logger.info('Processing new packet buffer')
    network_queue = []
    org_uuid = packets_buffer['origin']
    packets = [Packet(pkt) for pkt in packets_buffer['packets']]
    dest_uuid = getDestinationNetwork(org_uuid)
    with NetworkLock(dest_uuid) as net:
        net.process(packets)
        if net.reprocess:
            network_queue.append(net)
            net.reprocess = False
    altered_networks = processNetworkQueue(network_queue)
    publishAlteredNetworks(altered_networks)

def getDestinationNetwork(org_uuid):
    dest_uuid = getNetworkForOrigin(org_uuid)
    if not dest_uuid:
        net = Network.create()
        dest_uuid = net.uuid
        db_client.addNetwork(net.serialize())
        addOriginNetwork(dest_uuid, org_uuid)
    return dest_uuid

def publishAlteredNetworks(altered_networks):
    for uuid in altered_networks:
        network_data = db_client.db.networks.find_one({'uuid': uuid})
        if network_data:
            for device in network_data['devices']:
                mq_client.publish('device', device)

def mergeNetworks(to, fr, altered_networks):
    to.mergeNetwork(fr)
    altered_networks.append(to.uuid)
    altered_networks.remove(fr.uuid)
    db_client.deleteNetwork(fr.uuid)
    updateOriginNetwork(fr.uuid, to.uuid)

def processNetworkQueue(network_queue):
    if not network_queue:
        return []
    altered_networks = [network_queue[0].uuid]
    while network_queue:
        nex = network_queue.pop(0)
        with NetworkLock(nex.uuid):
            merge_uuid = findNetworkMatch(nex)
            if merge_uuid:
                with NetworkLock(merge_uuid) as merge_net:
                    mergeNetworks(merge_net, nex, altered_networks)
                    if merge_net.reprocess:
                        network_queue.append(merge_net)
                        merge_net.reprocess = False
    return altered_networks