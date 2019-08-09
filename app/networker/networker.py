import mlog
import env
import logging
import signal
import sys
import processor

from mqtt_client import MQTTClient
from db import DBClient

mlog.configLoggers(['main', 'network', 'proc', 'mqtt'], env.logs_folder, env.debug_mode)

mqtt = MQTTClient(env)
mongo = DBClient(env)

processor.mqtt = mqtt
processor.mongo = mongo

logger = logging.getLogger('main')
mqtt.on_topic('packetsBuffer', processor.processPacketsBuffer)
mqtt.on_topic('renameNetwork', processor.renameNetwork)
mqtt.on_topic('removeNetwork', processor.removeNetwork)
mqtt.on_topic('clearNetwork', processor.clearNetwork)

logger.info('Networker is up')
def _handleKill(self, signal, frame):
    mqtt.close()
    mongo.close()
    sys.exit(0)
signal.signal(signal.SIGINT, _handleKill)