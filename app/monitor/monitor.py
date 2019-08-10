import env
import sys
import time
sys.path.append(env.infra_path)

from mqtt_client import MQTTClient
from db import DBClient
import keepalive
import mlog
import logging
import threading
mlog.configLoggers(['main', 'mqtt'], env.logs_folder, env.debug_mode)

logger = logging.getLogger('main')

try:
    mqtt = MQTTClient(env)
    mongo = DBClient(env)
    def handleKeepAlive(kadata):
        global mongo
        comp = kadata['component']
        upd = {'name': comp, 'lts': time.time()}
        mongo.db.monitor.update_one(
            {'name': comp}, {'$set': upd},
            upsert=True
        )

    def pingDB():
        global mongo, mqtt
        while True:
            if mongo.ping():
                keepalive.beat(mqtt, 'DB')
            time.sleep(10)
    
    def handleJobStatus(jobdata):
        global mongo
        comp = jobdata['name']
        mongo.db.jobs.update_one(
            {'name': comp},
            {
                '$set': {
                    'name': comp,
                    'lts': time.time(),
                    'progress': jobdata['progress'],
                    'finished': jobdata['finished']
                }
            },
            upsert=True
        )
    mqtt.on_topic('keepalive', handleKeepAlive)
    mqtt.on_topic('job', handleJobStatus)
    
    dbThread = threading.Thread(target=pingDB)
    dbThread.daemon = True
    dbThread.start()

    keepalive.start(mqtt, 'monitor')
except KeyboardInterrupt:
    pass
except Exception, e:
    logger.fatal(str(e))
