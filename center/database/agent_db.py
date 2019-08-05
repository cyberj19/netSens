import logging
from infra import ProcessQueue
logger = logging.getLogger('db')
class AgentDB:
    def __init__(self, db, broker):
        self.db = db
        ProcessQueue('AgentWriter', 
            procFunc=self.writeAgent, 
            requeueOnFail=True,
            errorFunc=lambda e: logger.error(str(e)),
            preFunc=lambda l :l.serialize(),
            broker=broker,
            topic='agentUpdate')
	
    def get(self):
		return self.db['agents'].find()
		
    def getByNetworkId(self, networkId):
        return self.db['agents'].find({
            'networkId': networkId,
        })
        
    def writeAgent(self, agent):
        filt = {'mac': agent['mac'], 'mode': agent['mode']}
        self.db['agents'].upsert(filt, agent)