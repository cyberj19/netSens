import logging
import os
from importlib import import_module
logger = logging.getLogger('processor')

def load(mqc, dbc, lock):
    pnames = os.listdir('networker/processors')
    for pname in pnames:
        if pname in ['__init__.py', '__init__.pyc']:
            continue
        try:
            logger.info('loading processor %s', pname)
            module = import_module('processors.%s' % pname)
            Processor(mqc, dbc, lock, module)
        except Exception as e:
            logger.error('Failed to load processor: %s', str(e))

class Processor:
    def __init__(self, mqc, dbc, lock, module):
        self.logger = logger
        self.topic = module.topic
        self.proc_func = module.process
        module.init(mqc, dbc, lock, self.logger)
        mqc.on_topic(module.topic, self.process)

    def process(self, data):
        self.logger.info('new data on topic %s', self.topic)
        self.proc_func(data)