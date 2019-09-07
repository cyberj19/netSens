import pymongo
import threading

class DBClient:
    def __init__(self, env):
        self.client = pymongo.MongoClient(
                env.db_host, env.db_port
            )
        self.db = self.client[env.db_name]
        self.lock = threading.Lock()

    def ping(self):
        try:
            self.client.server_info()
            return True
        except Exception:
            return False
    def close(self):
        self.client.close()

    def getDevice(self, net_uuid, dev_uuid):
        net = self.db.networks.find_one({'uuid': net_uuid})
        if not net:
            return None
        for dev in net['devices']:
            if dev['uuid'] == dev_uuid:
                return dev
        return None
    def getNetworksOverview(self):
        return self.db.networks.aggregate([{
            '$project': {
                '_id': 0,
                'uuid': 1,
                'name': 1,
                'createTime': 1,
                'lastUpdateTime': 1,
                'defaultGTWMAC': 1,
                'deviceCount': {'$size': '$devices'},
                'linkCount': {'$size': '$links'},
                'packetCount': {'$size': '$packets'}
            }
        }])
        
    def getNetwork(self, uuid):
        return self.db.networks.find_one({'uuid': uuid},{'packets':0})
    def getDevicePackets(self, netUUID, devUUID):
        network = self.getNetwork(netUUID)
        if not network:
            return []
        packets = []
        for packet in network['packets']:
            for aspect in packet['aspects']:
                if 'source' in aspect and aspect['source']['uuid'] == devUUID:
                    packets.append(aspect)
                if 'target' in aspect and aspect['target']['uuid'] == devUUID:
                    packets.append(aspect)
        return packets
    def saveNetwork(self, network):
        self.db.networks.update(
            {'uuid': network['uuid']},
            {'$set': network},
            upsert=False
        )

    def deleteNetwork(self, uuid):
        self.db.networks.delete_one({
            'uuid': uuid
        })
    def addNetwork(self, network):
        self.db.networks.insert(network)