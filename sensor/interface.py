import os
import sys
import subprocess as subp
import logging
import env

logger = logging.getLogger('proxy')
def getInterfaces():
	if sys.platform == 'linux2':
		if env.sim_mode:
			return {'sim': 'AA:AA:AA:AA'}
		cmd="find /sys/class/net -mindepth 1 -maxdepth 1 ! -name lo -printf %P### -execdir cat {}/address ;"

		ifc_proc = subp.Popen(cmd.split(), stdout=subp.PIPE)
		#grp_proc = subp.Popen(['grep','HWaddr'], stdin=ifc_proc.stdout, stdout=subp.PIPE)
		#ifc_proc.stdout.close()
		
		ifaces = {}
		line = ifc_proc.stdout.readline().rstrip()
		while line:
			logger.debug('INTERFACE FILE: %s', line)
			parts = line.split("###")
			iface = parts[0]
			mac = parts[-1]
			ifaces[iface] = mac
			line = ifc_proc.stdout.readline().rstrip()
		return ifaces
	else:
		return []

def isInterfaceSupported(interface):
	return interface in getInterfaces()

def getDefaultGTW(iface):
	if sys.platform == 'linux2':
		with open('/proc/net/route') as fh:
			for line in fh:
				fields = line.strip().split()
				if fields[0] != iface:
					continue
				if fields[1] == '00000000':
					gtw = fields[2]
					gtw = gtw[0:2] + ':' + gtw[3:4] + ':' + gtw[5:6] + ':' + gtw[7:8]
					return gtw
			else:
				return None
	else:
		return None
