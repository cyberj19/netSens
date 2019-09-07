import env
import sys
sys.path.append(env.infra_path)

import mlog
from importlib import import_module
import os
import logging
from mq import MQClient
from db import DBClient
import time
import threading
import keepalive
import plugin
mlog.configLoggers(['main', 'mq', 'plugin', 'db'], env.logs_folder, env.debug_mode)
logger = logging.getLogger('main')
try:
    mqc = MQClient(env)
    dbc = DBClient(env)
    plugin.load(mqc, dbc, env)
    keepalive.start(mqc, 'thirdpary')
except KeyboardInterrupt:
    pass    
except Exception as e:
    logger.critical(str(e))
    