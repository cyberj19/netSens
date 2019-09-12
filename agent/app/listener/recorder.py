import threading
import time
import subprocess
import os
import platform
import logging
logger = logging.getLogger('agent')
class Recorder:
    def __init__(self, env, queue):
        self.thread = threading.Thread(target=self.record)
        self.thread.setDaemon(True)

        self.queue = queue

        self.env = env
        logger.info('Recorder is ready')
    def start(self):
        self.thread.start()
        logger.debug('Recorder has started')

    def record(self):
        while True:
            ts = time.time()
            filename = "%s-%d.pcap" % (self.env.uuid, ts)
            filepath = os.path.join(self.env.output_folder, filename)
            cmd = self.getCommand(filepath)
            subprocess.call(cmd)
            self.queue.enqueue({'ts': ts, 'path': filepath})

    def getCommand(self, filepath):
        if platform.system() == "Linux":
            return ["sudo", 
                    "timeout", str(self.env.capture_interval), 
                    "tcpdump",
                    "-i", self.env.iface,
                    "-w", filepath] 
        elif platform.system() == "Windows":
            return [self.env.shark_path,
                    "-i", self.env.iface,
                    "-F", "pcap",
                    "-w", filepath,
                    "-a", "duration:%d" % self.env.capture_interval]