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