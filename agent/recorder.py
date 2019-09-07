import threading
import time
import subprocess
import os

class Recorder:
    def __init__(self, env, queue):
        self.thread = threading.Thread(target=self.record)
        self.thread.setDaemon(True)

        self.queue = queue

        self.env = env

    def start(self):
        self.thread.start()

    def record(self):
        while True:
            ts = time.time()
            filename = "%s-%d.pcap" % (self.env.uuid, ts)
            filepath = os.path.join(self.env.output_folder, filename)
            cmd = ["sudo", 
                    "timeout", str(self.env.capture_interval), 
                    "tcpdump",
                    "-i", self.env.iface,
                    "-w", filepath]
            subprocess.call(cmd)
            self.queue.enqueue({'ts': ts, 'path': filepath})