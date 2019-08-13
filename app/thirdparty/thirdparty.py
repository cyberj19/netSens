import env
import sys
sys.path.append(env.infra_path)

import mlog
from importlib import import_module
import os
import logging
from mqtt_client import MQTTClient
from db import DBClient
from plugin import Plugin
import time
import threading
import keepalive
mlog.configLoggers(['main', 'mqtt'], env.logs_folder, env.debug_mode)
logger = logging.getLogger('main')
try:
    mqtt = MQTTClient(env)
    mongo = DBClient(env)
    pluginNames = os.listdir('plugins')
    logger.debug(pluginNames)
    for pluginName in pluginNames:
        if pluginName == '__init__.py' or \
            pluginName == '__init__.pyc': 
            continue
        try:
            logger.info('Loading plugin %s', pluginName)
            mdl = import_module('plugins.' + pluginName)
            mlog.configLoggers([mdl.name], env.logs_folder, env.debug_mode)
            Plugin(mdl, mqtt, mongo)
        except Exception as e:
            logger.error('Failed to load plugin: %s', str(e))
    keepalive.start(mqtt, 'thirdpary')
except KeyboardInterrupt:
    pass    
except Exception as e:
    logger.critical(str(e))
    