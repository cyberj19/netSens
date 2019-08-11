import os
import subprocess
import sys
import shutil

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

# prepare env file for web.py
if len(sys.argv) == 1:
	env_file = 'public'
else:
	env_file = sys.argv[1]

shutil.copyfile('app/web/env_%s.py' % env_file, 'app/web/env.py')

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