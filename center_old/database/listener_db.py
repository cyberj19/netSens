import logging
from infra import ProcessQueue
logger = logging.getLogger('db')
class ListenerDB:
    def __init__(self, db, broker):
        self.db = db
        ProcessQueue('ListenerWriter', 
            procFunc=self.writeListener, 
            requeueOnFail=True,
            errorFunc=lambda e: logger.error(str(e)),
            preFunc=lambda l :l.serialize(),
            broker=broker,
            topic='listenerUpdate')
	
    def get(self):
		return self.db['listeners'].find()
		
    def getByNetworkId(self, networkId):
        return self.db['listeners'].find({
            'networkId': networkId,
        })
        
    def writeListener(self, lstr):
        filt = {'mac': lstr['mac']}
        self.db['listeners'].upsert(filt,lstr)