import env
import sys
import time
sys.path.append(env.infra_path)

from mq import MQClient
from db import DBClient
import keepalive
import mlog
import logging
import threading
mlog.configLoggers(['main', 'mq'], env.logs_folder, env.debug_mode)

logger = logging.getLogger('main')

try:
    mqc = MQClient(env)
    dbc = DBClient(env)
    def handleKeepAlive(kadata):
        comp = kadata['component']
        upd = {'name': comp, 'lts': time.time()}
        dbc.db.monitor.update_one(
            {'name': comp}, {'$set': upd},
            upsert=True
        )

    def pingDB():
        while True:
            if dbc.ping():
                keepalive.beat(mqc, 'DB')
            time.sleep(10)
    
    mqc.on_topic('keepalive', handleKeepAlive)
    
    dbThread = threading.Thread(target=pingDB)
    dbThread.daemon = True
    dbThread.start()

    keepalive.start(mqc, 'monitor')
except KeyboardInterrupt:
    pass
except Exception as e:
    logger.fatal(str(e))