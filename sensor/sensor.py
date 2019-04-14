import mlog
import logging
import env
import proxy
import sys
import signal

logger = logging.getLogger('sensor')

def handleKill(signal, frame):
	logger.warning('sensor killed by user')
	sys.exit(0)
signal.signal(signal.SIGINT, handleKill)

if env.sim_mode:
	logger.info('RUNNING IN SIMULATION MODE')

prx = proxy.Proxy(env.id, 
				env.comm_iface, env.local_port,
				env.center_ip, env.center_port)
				
	