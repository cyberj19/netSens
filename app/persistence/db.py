import pymongo
import threading

class DB:
    def __init__(self, env):
        self.client = pymongo.MongoClient(
                env.db_host, env.db_port
            )
        self.db = self.client[env.db_name]
        self.lock = threading.Lock()