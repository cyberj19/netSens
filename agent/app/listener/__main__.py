import env
import time
import threading
from uuid import getnode as get_mac
from recorder import Recorder
from sender import Sender
from filequeue import FileQueue

import mlog
import logging
mlog.configLoggers(['agent'], logs_folder=env.logs_folder, debug_mode=env.debug_mode)
logger = logging.getLogger('agent')
env.uuid = '%s.%s' % (env.iface, str(get_mac()))

queue = FileQueue(env)

sender = Sender(env, queue)
sender.start()

if env.mode == "live":
    recorder = Recorder(env, queue)
    recorder.start()
logger.info('Agent %s is up in %s mode', env.uuid, env.mode)


while True:
    time.sleep(1)
