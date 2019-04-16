import logging
from infra import ProcessQueue
logger = logging.getLogger('db')
class DeviceDB:
    def __init__(self, db, broker):
        self.db = db
        ProcessQueue('DeviceWriter', 
            procFunc=self.writeDevice, 
            requeueOnFail=True,
            errorFunc=lambda e: logger.error(str(e)),
            preFunc=lambda d: d.serialize(),
            broker=broker,
            topic='deviceUpdate')
	
    def get(self):
		return self.db['devices'].find()
		
    def getById(self, networkId, deviceId):
        logger.debug('getting device %d network %d', deviceId, networkId)
        device = self.db['devices'].find_one({
            'networkId': networkId,
            'id': deviceId
        })
        logger.debug(str(device))
        return device
    def getByNetworkId(self, networkId):
        devices = self.db['devices'].find({'networkId': networkId})
        return devices
        
    def writeDevice(self, device):
        filt = {'id': device['id'], 'networkId': device['networkId']}
	if device['vendor'] == "ADB Italia":
		logger.debug("FYA %s", str(device))
        self.db['devices'].upsert(filt,device)
