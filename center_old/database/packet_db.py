import logging
from infra import ProcessQueue
logger = logging.getLogger('db')

class PacketDB:
    def __init__(self, db, broker):
        self.db = db
        ProcessQueue('PacketWriter', 
            procFunc=lambda pa: self.db['packets'].insert_many(pa), 
            bulkMode=True,
            requeueOnFail=True,
            preFunc=lambda p: p.serialize(),
            broker=broker,
            topic='packetProcessed',
            interval=10)
    
    def getPackets(self):
        return self.db['packets'].find()

    def getByDeviceId(self, networkId, deviceId):
        sarps = self.db['packets'].find({
            'networkId': networkId,
            'sourceDeviceId': deviceId
        })
        tarps = self.db['packets'].find({
            'networkId': networkId,
            'targetDeviceId': deviceId
        })
        arps = sarps + tarps
        logger.debug(str(arps))
        return arps