import logging
from infra import ProcessQueue
logger = logging.getLogger('db')
class SourceDB:
    def __init__(self, db, broker):
        self.db = db
        self.db['sources'].delete()
        ProcessQueue('SourceWriter', 
            procFunc=self.writeSource, 
            requeueOnFail=True,
            errorFunc=lambda e: logger.error(str(e)),
            preFunc=lambda s :s.serialize(),
            broker=broker,
            topic='listenerUpdate')
	
    # def delete(self):
    #     self.db['listeners'].delete()

    def get(self):
		return self.db['sources'].find()
		
    def getByNetworkId(self, networkId):
        return self.db['sources'].find({
            'networkId': networkId,
        })
        
    def writeSource(self, lstr):
        filt = {'guid': lstr['guid']}
        self.db['sources'].upsert(filt,lstr)