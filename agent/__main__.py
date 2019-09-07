import env
import urllib3
import time
import subprocess
import os
from uuid import getnode as get_mac
import threading
origin_uuid = '%s-%s' % (env.iface, str(get_mac()))
queue = []
lock = threading.Lock()

def write():
    while True:
        filename = "%s-%d.pcap" % (origin_uuid, time.time())
        filename = os.path.join(env.output_folder, filename)
        cmd = [env.shark_path,
                "-i", env.iface,
                "-w", filename,
                "-a", "duration:%d" % env.capture_interval]
        subprocess.call(cmd)
        with lock:
            queue.append(filename)


def upload(filename):
    with open(filename, 'rb') as fp:
        data = fp.read()
    urllib3.http.request(
        'POST',
        '%s:%d/api/upload/%s' % (env.gtw_host, env.gtw_port, origin_uuid),
        fields={
            'file': ()
        }
    )

def read():
    while True:
        item = None
        with lock:
            if queue:
                item = queue.pop(0)
        if item:
            upload(item)