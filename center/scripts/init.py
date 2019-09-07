import os
import subprocess
import sys
import shutil
import json
import platform

service_file = "services.%s.json" % platform.system().lower()
with open(service_file, 'r') as fp:
	services = json.load(fp)
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
	'data/logs/thirdparty'
]

for d in dirlist:
	dir = os.path.join(root_dir, d)
	if not os.path.exists(dir):
		print 'creating dir: %s' % dir
		os.mkdir(dir)

# prepare env file for web.py
if len(sys.argv) == 1:
	env_file = 'public'
else:
	env_file = sys.argv[1]

shutil.copyfile('app/web/env_%s.py' % env_file, 'app/web/env.py')



for service in services:
	print 'starting service: %s' % service['name']
	os.chdir(service['execPath'])
	cmd = service['cmd'].replace('%rd%', root_dir).split(' ')
	subprocess.Popen(cmd, shell=True)
	os.chdir(root_dir)