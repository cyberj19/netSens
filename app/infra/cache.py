import time
import threading
class Cache:
    def __init__(self, mongoClient, dbName, collName,
                        maxStoreSize=10,
                        maxValidTime=10):
        self.conn = mongoClient[dbName][collName]
        self.store = {}
        self.store_size = 0
        self.max_size = maxStoreSize
        self.max_valid_time = maxValidTime
    
    def get(self, uuid):
        if not uuid in self.store:
            self.create_item(uuid)
        return self.store[uuid].get()
    
    def create_item(self, uuid):
        if self.store_size == self.max_size:
            self.purge_oldest()
        self.store[uuid] = CacheItem(uuid, self.max_valid_time, self.conn)
        self.store_size += 1

    def purge_oldest(self):
        oldest = None
        for uuid in self.store:
            if not oldest or self.store[uuid].time < oldest.time:
                oldest = self.store[uuid]
        if oldest:
            self.store[oldest.uuid].save()
            del self.store[oldest.uuid]
            self.store_size -= 1
                
class CacheItem:
    def __init__(self, uuid, max_valid_time, conn):
        self.max_valid_time = max_valid_time
        self.conn = conn
        self.uuid = uuid
        self.data = None
        self.time = None

    def load(self):
        self.data = self.conn.find_one({'uuid': self.uuid})
        self.time = time.time()

    def save(self):
        if not self.data: return
        
        self.conn.update_one(
            {'uuid': self.uuid}, 
            {'$set': self.data}, 
            upsert=True
        )

    def get(self):
        if not self.time or \
            self.time < time.time() - self.max_valid_time:
            self.load()
        return self.data