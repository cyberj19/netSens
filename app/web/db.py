import pymongo
import threading
import logging

logger = logging.getLogger('db')

class DBClient:
    def __init__(self, env):
        self.client = pymongo.MongoClient(
                env.mongo_host, env.mongo_port
            )
        self.db = self.client[env.mongo_db_name]
        self.lock = threading.Lock()
        logger.info('DBClient initiated: %s:%d/%s', 
                    env.mongo_host, env.mongo_port, env.mongo_db_name)

def strip_id(docs):
    sdocs = []
    for doc in docs:
        del doc['_id']
        sdocs.append(doc)
    return sdocs