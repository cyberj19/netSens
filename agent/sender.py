from mq import MQClient
import threading
import os

class Sender:
    def __init__(self, env, queue):
        self.mq_client = MQClient(env)
        self.thread = threading.Thread(target=self.send)
        self.thread.setDaemon(True)
        self.queue = queue
        self.env = env

    def start(self):
        self.thread.start()
    
    def send(self):
        while True:
            try:
                item = self.queue.dequeue()
                if item:
                    self.upload(item)
                time.sleep(self.env.capture_interval)
            except Exception as e:
                print str(e)

    def upload(self, file):
        with open(file['path'], 'rb') as fp:
            data = fp.read()
        msg = {
            'time': file['ts'],
            'origin': env.uuid,
            'data': base64.b64encode(data).decode('utf-8')
        }
        self.mq_client.publish('livePCAP', msg)
        if self.env.mode == "live":
            # remove file
            os.remove(file['path'])