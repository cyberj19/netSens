import sys
import env
import time
import mlog
from models.network import loadNetwork
from processor import MainProcessor
from infra import Broker
from gtw import GTW
from database import DB
from api import WebServer
from services import fingerbank as fbank

import logging
import traceback
logger = logging.getLogger('main')

try:
	broker = Broker()
	fbank.setup(broker)
	db = DB(broker)
	gtw = GTW(env, broker)
	networkFile = db.getNetworks()
	networks = [loadNetwork(ntw) for ntw in networkFile]
	logger.info('Loaded %d networks from DB', len(networks))
	proc = MainProcessor(networks, broker)
	web = WebServer(env.flask_port, db, gtw, broker)
except Exception, e:
	logger.fatal('Fatal error: %s', str(e))
	traceback.print_exc()
	sys.exit()