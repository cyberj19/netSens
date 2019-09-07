import env
import urllib3
import time
import subprocess
import os
import mq
import base64
from uuid import getnode as get_mac
import threading
origin_uuid = '%s.%s' % (env.iface, str(get_mac()))
queue = []
lock = threading.Lock()

mq_client = mq.MQClient(env)
def write():
    while True:
        filename = "%s-%d.pcap" % (origin_uuid, time.time())
        filename = os.path.join(env.output_folder, filename)
        print 'writing file %s' % filename
        cmd = ["sudo", "timeout", str(env.capture_interval), "tcpdump",
                "-i", env.iface,
                "-w", filename]
        print cmd
        subprocess.call(cmd)
        with lock:
            queue.append(filename)
write_thread = threading.Thread(target=write)
write_thread.setDaemon(True)
write_thread.start()

def upload(filename):
    ts = filename.split('-')[1].split('.')[0]
    with open(filename, 'rb') as fp:
        data = fp.read()
    msg = {
        'time': float(ts),
        'origin': origin_uuid,
        'data': base64.b64encode(data).decode('utf-8')
    }
    mq_client.publish('livePCAP', msg)

    

def read():
    while True:
        try:
            item = None
            with lock:
                if queue:
                    item = queue.pop(0)
            if item:
                print 'uploading %s' % item
                upload(item)
        except Exception as e:
            print str(e)
read_thread = threading.Thread(target=read)
read_thread.setDaemon(True)
read_thread.start()

while True:
    time.sleep(1)
