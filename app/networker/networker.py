import env
import sys
sys.path.append(env.infra_path)

import logging
import signal
import processor
import keepalive

from mqtt_client import MQTTClient
from db import DBClient
import mlog

mlog.configLoggers(['main', 'network', 'proc', 'mqtt'], env.logs_folder, env.debug_mode)
logger = logging.getLogger('main')

try:
    mqtt = MQTTClient(env)
    mongo = DBClient(env)

    processor.mqtt = mqtt
    processor.mongo = mongo

    mqtt.on_topic('packetsBuffer', processor.processPacketsBuffer)
    mqtt.on_topic('renameNetwork', processor.renameNetwork)
    mqtt.on_topic('removeNetwork', processor.removeNetwork)
    mqtt.on_topic('clearNetwork', processor.clearNetwork)
    mqtt.on_topic('deviceExtraData', processor.addDeviceExtraData)

    logger.info('Networker is up')
    keepalive.start(mqtt, 'networker')
except KeyboardInterrupt:
    pass
except Exception, e:
    logger.fatal(str(e))