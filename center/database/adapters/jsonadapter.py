import json
import threading
import os
import logging

logger = logging.getLogger('db')

class JsonAdapter:
    def __init__(self, env):
        self.folder = env.db_folder
        if not os.path.exists(self.folder):
            os.mkdir(self.folder)
        self.tables = {}
    
    def close(self):
        for tbl in self.tables:
            self.tables[tbl].close()

    def __getitem__(self, name):
        if name in self.tables:
            return self.tables[name]
        self.tables[name] = Table(self.folder, name)
        return self.tables[name]

def _match_filter(doc, filter):
    for key in filter:
        if not key in doc:
            return False
        if not doc[key] == filter[key]:
            return False
    return True

class Table:
    def __init__(self, folder, name):
        self.file = '%s/%s.json' % (folder, name)
        self.lock = threading.Lock()
        self.closed = False
        self.table = None

    def close(self):
        with self.lock:
            self.closed = True
    
    
    def insert_many(self, docs):
        with self.lock:
            if self.closed:
                logger.warning('Data not writted to DB')
                return
            self.get()
            for doc in docs:
                self.table.append(doc)
            self.save()
    
    def find_one(self, filter):
        with self.lock:
            if self.closed:
                logger.warning('DB is closed')
                return None
            self.get()
        # logger.debug('Filter: %s', str(filter))
        for doc in self.table:
            # logger.debug('matching doc : %s', str(doc))
            if _match_filter(doc, filter):
                # logger.debug('matched doc: %s', str(doc))
                return doc
        return None
    
    def find(self, filter=None):
        with self.lock:
            if self.closed:
                logger.warning('DB is closed')
                return []
            self.get()
        # logger.debug('Filter: %s', str(filter))
        if filter:
            docs = [doc for doc in self.table if _match_filter(doc,filter)]
        else:
            docs = self.table
        return docs

    def delete(self, filter=None):
        with self.lock:
            if self.closed:
                logger.warning('Data was not updated in DB')
                return
            self.get()
            if filter:
                for i, doc in enumerate(self.table):
                    if _match_filter(doc, filter):
                        del self.table[i]
            else:
                self.table = []
            self.save()

    def upsert(self, filter, newDoc):
        with self.lock:
            if self.closed:
                logger.warning('Data was not written to DB')
                return
            self.get()
            for i, doc in enumerate(self.table):
                if _match_filter(doc, filter):
                    self.table[i] = newDoc
                    break
            else:
                self.table.append(newDoc)
            self.save()
        
    def get(self):
        if not os.path.exists(self.file):
            self.table = []
            return
        with open(self.file,'r') as fp:
            self.table = json.load(fp)
    
    def save(self):
        with open(self.file,'w') as fp:
            json.dump(self.table, fp)
