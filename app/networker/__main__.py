import env
import sys
sys.path.append(env.infra_path)
sys.path.append('models')
sys.path.append('entities')

from importlib import import_module
import logging
import signal
import keepalive
import network_lock
from mq import MQClient
from db import DBClient

import mlog
import os
import processor

mlog.configLoggers(['main', 'network', 'proc', 'mq', 'db', 'model'], env.logs_folder, env.debug_mode)
logger = logging.getLogger('main')

try:
    mqc = MQClient(env)
    dbc = DBClient(env)
    network_lock.init(dbc)
    processor.load(mqc, dbc, network_lock.lock)
    logger.info('Networker is up')
    keepalive.start(mqc, 'networker')
except KeyboardInterrupt:
    pass
except Exception as e:
    logger.fatal(str(e))