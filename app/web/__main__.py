import env
import sys
sys.path.append(env.infra_path)
import mlog
import logging
import time
from mq import MQClient 
from api_server import APIServer
from db import DBClient

mlog.configLoggers(['main', 'mq', 'api', 'db', 'endpoint'], env.logs_folder, env.debug_mode)

logger = logging.getLogger('main')

try:
    mqc = MQClient(env)
    dbc = DBClient(env)
    api = APIServer(env, mqc, dbc)
    logger.info('WEB Server up and running')

    api.start()
except KeyboardInterrupt:
    pass
except Exception as e:
    logger.fatal(str(e))

