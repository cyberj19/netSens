import logging
logger = logging.getLogger('processor')
class Processor:
    def __init__(self, mqtt, mongo, nlock, module):
        module.init(mqtt, mongo, nlock, logger)
        mqtt.on_topic(module.topic, module.process)