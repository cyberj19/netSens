import os
import subprocess

os.chdir('..')
root_dir = os.getcwd()
dirlist = [
	'data',
	'data/mongo',
	'data/playback',
	'data/runtime',
	'data/runtime/playback',
	'data/runtime/monitor',
	'data/runtime/web',
	'data/runtime/networker',
	'data/logs',
	'data/logs/playback',
	'data/logs/monitor',
	'data/logs/web',
	'data/logs/networker',
]

for d in dirlist:
	dir = os.path.join(os.getcwd(), d)
	if not os.path.exists(dir):
		print 'creating dir: %s' % dir
		os.mkdir(dir)
		
services = [
	['MONGO', 'C:\\Program Files\\MongoDB\\Server\\3.6\\bin', 'mongod.exe', '--dbpath', os.path.join(os.getcwd(),'data/mongo')],
	['MOSQUITTO', 'C:\\Program Files\\mosquitto','mosquitto.exe'],
	['WEB', 'app/web','python', 'web.py'],
	['PLAYBACK', 'app/playback', 'python', 'playback.py'],
	['NETWORKER', 'app/networker', 'python', 'networker.py'],
	['MONITOR', 'app/monitor', 'python', 'monitor.py']
]

for service in services:
	print 'starting service: %s' % service[0]
	os.chdir(service[1])
	subprocess.Popen(service[2:], shell=True)
	os.chdir(root_dir)