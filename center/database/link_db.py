import logging
from infra import ProcessQueue
logger = logging.getLogger('db')

class LinkDB:
    def __init__(self, db, broker):
        self.db = db
        ProcessQueue('LinkWriter', 
            procFunc=self.writeLink, 
            errorFunc=lambda e: logger.error('Failed writing links: %s', str(e)),
            requeueOnFail=True,
            preFunc=lambda l: l.serialize(),
            broker=broker,
            topic='linkUpdate')
    
    def getLinks(self):
        return self.db['links'].find()
    
    def getByNetworkId(self, networkId):
        return self.db['links'].find({'networkId': networkId})

    def writeLink(self, lnk):
        logger.info('Writing link %d to db', lnk['id'])
        filt = {'id': lnk['id'], 'networkId': lnk['networkId']}            
        self.db['links'].upsert(filt,lnk)