import threading
import time
class FileQueue:
    def __init__(self, env):
        if env.mode == "live":
            self.queue = []
            self.lock = threading.Lock()
        elif env.mode == "test":
            self.queue = env.test_file
        self.env = env
    
    def enqueue(self, item):
        if self.env.mode == "live":
            with self.lock:
                self.queue.append(item)

    def dequeue(self):
        if self.env.mode == "live":
            with self.lock:
                if self.queue:
                    return self.queue.pop(0)
                else:
                    return None
        elif self.env.mode == "test":
            return {
                "ts": time.time(),
                "path": self.queue
            }