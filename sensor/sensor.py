import env
import sys
import logging
import signal
import api

from source_manager import SourceManager
from center_proxy import CenterProxy
from infra.broker import Broker
from infra import mlog


mlog.createLoggers(['sensor', 'api', 'centerProxy', 'playbackSource', 'liveSource', 'SourceManager'])
logger = logging.getLogger('sensor')

env.mode = sys.argv[1]
logger.info('Running in %s mode', env.mode)

broker = Broker()
proxy = CenterProxy(env, broker)
manager = SourceManager(env, broker)


def handleKill(signal, frame):
	logger.warning('sensor killed by user')
	proxy.stop()
	sys.exit(0)
signal.signal(signal.SIGINT, handleKill)

api.API(env, manager)

