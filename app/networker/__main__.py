import env
import sys
sys.path.append(env.infra_path)
sys.path.append('models')

from importlib import import_module
import logging
import signal
import keepalive
import network_lock
from mqtt_client import MQTTClient
from db import DBClient

import mlog
import os
from processor import Processor
mlog.configLoggers(['main', 'network', 'proc', 'mqtt'], env.logs_folder, env.debug_mode)
logger = logging.getLogger('main')

try:
    mqtt = MQTTClient(env)
    mongo = DBClient(env)
    network_lock.init(mongo)

    pnames = os.listdir('networker/processors')
    for pname in pnames:
        if pname in ['__init__.py', '__init__.pyc']:
            continue
        try:
            logger.info('loading processor %s', pname)
            module = import_module('processors.%s' % pname)
            Processor(mqtt, mongo, network_lock.lock, module)
        except Exception as e:
            logger.error('Failed to load processor: %s', str(e))

    logger.info('Networker is up')
    keepalive.start(mqtt, 'networker')
except KeyboardInterrupt:
    pass
except Exception as e:
    logger.fatal(str(e))