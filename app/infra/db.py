import pymongo
import threading

class DBClient:
    def __init__(self, env):
        self.client = pymongo.MongoClient(
                env.mongo_host, env.mongo_port
            )
        self.db = self.client[env.mongo_db_name]
        self.lock = threading.Lock()

    def ping(self):
        try:
            self.client.server_info()
            return True
        except Exception:
            return False
    def close(self):
        self.client.close()

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
        return self.db.networks.find_one({'uuid': uuid})

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