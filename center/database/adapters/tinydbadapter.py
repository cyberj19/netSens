from tinydb import TinyDB, where
import logging
import threading

logger = logging.getLogger('DB')
class TinyDBAdapter:
    def __init__(self, env):
        self.db = TinyDB(env.db_file)
        self._lock = threading.Lock()

    def close(self):
        with self._lock:
            self.db.close()

    def upsert(self, tblName, filter, doc):
        try:
            tbl  = self.db.table(name=tblName)
            cond = self._comb_cond(filter)
            with self._lock:
                tbl.upsert(doc,cond)
        except Exception, e:
            logger.error('Unable to upsert: %s', str(e))

    def insert_many(self, tblName, docs):
        try:
            tbl = self.db.table(name=tblName)
            with self._lock:
                tbl.insert_multiple(docs)
        except Exception, e:
            logger.error('Unable to insert many: %s', str(e))

    def find_one(self, tblName, filter):
        try:
            tbl = self.db.table(name=tblName)
            cond = self._comb_cond(filter)
            return tbl.get(cond)
        except Exception, e:
            logger.error('Unable to find one: %s', str(e))

    def find(self, tblName, filter=None):
        try:
            tbl = self.db.table(name=tblName)
            if not filter:
                return tbl.all()
            cond = self._comb_cond(filter)
            return tbl.search(cond)
        except Exception, e:
            logger.error('Unable to find many: %s', str(e))

    def _comb_cond(self, filter):
        filter_params = filter.keys()

        param = filter_params[0]
        logger.debug('tiny where(\'{0}\').exists() & where(\'{0}\').__eq__({1})'
                    .format(param, str(filter[param])))

        cond = where(param).exists() & \
            where(param).__eq__(filter[param])
        for param in filter_params[1:]:
            
            logger.debug('tiny where(\'{0}\').exists() & where(\'{0}\').__eq__({1})'
                        .format(param, str(filter[param])))

            cond = cond & \
                    where(param).exists() & \
                    where(param).__eq__(filter[param])
        return cond