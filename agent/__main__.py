import env
import time
import threading
from uuid import getnode as get_mac
from recorder import Recorder
from sender import Sender
from filequeue import FileQueue
env.uuid = '%s.%s' % (env.iface, str(get_mac()))

queue = FileQueue(env)

if env.mode == "live":
    recorder = Recorder(env, queue)
    recorder.start()

sender = Sender(env, queue)
sender.start()

while True:
    time.sleep(1)
