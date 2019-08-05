import pymongo
import logging
import threading
logger = logging.getLogger('DB')

class MongoDBAdapter:
    def __init__(self, env):
        try:
			if not env.db_auth:
				mongo = pymongo.MongoClient(env.db_host, env.db_port)
			else:
				mongo = pymongo.MongoClient(env.db_host,env.db_port,
													username = env.db_user,
													password = env.db_pass)
        except Exception,e:
            raise e
        self.conn = mongo
        self.db = mongo[env.db_name]
        self._lock = threading.Lock()

    def close(self):
        with self._lock:
            self.conn.close()

    def upsert(self, tblName, filter, doc):
        try:
            tbl = self.db[tblName]
            with self._lock:
                tbl.update_one(filter,{'$set':doc},upsert=True)
        except Exception, e:
            logger.error('Trying to upsert doc %s', str(doc))
            logger.error('Error: %s', str(e))

    def insert_many(self, tblName, docs):
        try:
            with self._lock:
                self.db[tblName].insert_many(docs)
        except Exception, e:
            logger.error('Unable to insert many: %s', str(e))

    def find_one(self, tblName, filter):
        try:
            doc = self.db[tblName].find_one(filter)
            if doc:
                del doc['_id']
            return doc
        except Exception, e:
            logger.error('Unable to find: %s', str(e))

    def find(self, tblName, filter=None):
        try:
            if not filter:
                return _strip_id(self.db[tblName].find())
            else:
                return _strip_id(self.db[tblName].find(filter))
        except Exception, e:
            logger.error('Failed to execute find: %s', str(e))
            
def _strip_id(docs):
    sdocs = []
    for doc in docs:
        del doc['_id']
        sdocs.append(doc)
    return sdocs