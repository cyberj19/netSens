import mlog
import logging
import env
import proxy
import sys
import signal
import os

logger = logging.getLogger('sensor')

def handleKill(signal, frame):
	logger.warning('sensor killed by user')
	sys.exit(0)
signal.signal(signal.SIGINT, handleKill)

if env.sim_mode:
	logger.info('RUNNING IN SIMULATION MODE')

if not os.path.exists(env.recs_folder):
	os.makedirs(env.recs_folder)
prx = proxy.Proxy(env.id, 
				env.comm_iface, env.local_port,
				env.center_ip, env.center_port)
				
	
