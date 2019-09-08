import os
import subprocess
import sys
import shutil
import json
import platform

os.chdir('..')
root_dir = os.getcwd()
dirlist = [
	'runtime',
	'runtime/data',
	'runtime/data/listener',
	'runtime/logs',
	'runtime/logs/listener'
]

for d in dirlist:
	dir = os.path.join(root_dir, d)
	if not os.path.exists(dir):
		print 'creating dir: %s' % dir
		os.mkdir(dir)

os.chdir('app')
cmd = ['python', 'listener']
subprocess.Popen(cmd, shell=True)