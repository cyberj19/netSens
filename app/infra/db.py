import pymongo
import threading

class DBClient:
    def __init__(self, env):
        self.client = pymongo.MongoClient(
                env.mongo_host, env.mongo_port
            )
        self.db = self.client[env.mongo_db_name]
        self.lock = threading.Lock()

    def close(self):
        self.client.close()

    def getNetworksOverview(self):
        return self.db.networks.find(
            {},
            {'uuid':1, 'defaultGTWMAC':1}
        )
    
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