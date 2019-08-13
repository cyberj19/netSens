import threading
import time
import logging

class Plugin:
    def __init__(self, module, mqtt, mongo):
        self.logger = logging.getLogger(module.name)
        self.module = module
        self.mqtt = mqtt
        self.mongo = mongo
        self.mqtt.on_topic('plugin-device-%s' % self.module.uuid, self.manual_process_device)
        self.mqtt.on_topic('device', self.process_device)
        
        self.module.setLogger(self.logger)
        thread = threading.Thread(target=self.publish)
        thread.daemon = True
        thread.start()
    def publish(self):
        while True:
            self.desc = {
                'uuid': self.module.uuid,
                'name': self.module.name,
                'level': self.module.level,
                'lastUpdateTime': time.time()
            }
            self.mongo.db.plugins.update_one(
                {'uuid': self.module.uuid},
                {'$set': self.desc}, 
                upsert=True
            )
            time.sleep(10)

    def process_device(self, device, manual=False):
        extraData = self.module.processDevice(device, manual)
        
        if extraData:
            self.mqtt.publish('deviceExtraData', {
                'networkUUID': device['networkId'],
                'deviceUUID': device['uuid'],
                'extraData': extraData
            })
    
    def manual_process_device(self, device):
        self.logger.info('manual device process')
        self.process_device(device, manual=True)