import threading
import time

class ProcessQueue:
    def __init__(self, name, procFunc,
                preFunc=None, 
                errorFunc=None, 
                bulkMode=False,
                requeueOnFail=False,
                broker=None, 
                topic=None,
                interval=-1):
        self.procFunc = procFunc
        self.preFunc = preFunc
        self.errorFunc = errorFunc
        self.bulkMode = bulkMode
        self.requeueOnFail = requeueOnFail
        self.interval = interval
        if broker and topic:
            broker.on(topic, self.enqueue)
    
        self.queue = []
        self.lock = threading.Lock()
        self.thread = threading.Thread(
            target = self.process,
            name = name
        )
        self.thread.setDaemon(True)
        self.thread.start()
    def purge(self):
        with self.lock:
            self.queue = []
    def enqueue(self, data):
        if self.preFunc:
            try:
                data = self.preFunc(data)
            except Exception, e:
                if self.errorFunc:
                    self.errorFunc(e)
                return
        with self.lock:
            self.queue.append(data)
    
    def process(self):
        while True:
            if not self.queue:
                continue
            with self.lock:
                if self.bulkMode:
                    data = self.queue
                    self.queue = []
                else:
                    data = self.queue[0]
                    self.queue = self.queue[1:]
            
            try:
                self.procFunc(data)
            except Exception, e:
                if self.requeueOnFail:
                    if self.bulkMode:
                        self.queue = data
                    else:
                        self.queue = [data] + self.queue
                if self.errorFunc:
                    self.errorFunc(e)
            if self.interval != -1:
                time.sleep(self.interval)