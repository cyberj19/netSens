import env
import sys
sys.path.append(env.infra_path)
import mlog
import logging
import time
from mqtt_client import MQTTClient 
from api_server import APIServer
from db import DBClient

mlog.configLoggers(['main', 'mqtt', 'api', 'db', 'endpoint'], env.logs_folder, env.debug_mode)

logger = logging.getLogger('main')

try:
    mqtt = MQTTClient(env)
    mongo = DBClient(env)
    api = APIServer(env, mqtt, mongo)
    logger.info('WEB Server up and running')

    api.start()
except KeyboardInterrupt:
    pass
except Exception,e:
    logger.fatal(str(e))

