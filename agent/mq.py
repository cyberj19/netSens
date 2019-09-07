import threading
import logging
import paho.mqtt.client as mqtt
import json
logger = logging.getLogger('mq')

class MQClient:
    def __init__(self, env):
        self.host = env.mq_host
        self.port = env.mq_port
        self.client = mqtt.Client()
        self.subscribers = {}
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.connect(self.host, self.port, 60)
        loop = threading.Thread(target=self.client.loop_forever)
        loop.daemon = True
        loop.start()

    def close(self):
        self.client.close()
        logger.info('Closed connection to broker')
    def on_topic(self, topic, func):
        if not topic in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(func)
        self.client.subscribe(topic)
    def on_connect(self, client, userdata, flags, rc):
        logger.info("Connected with result code %s", str(rc))

    def on_message(self, client, userdata, msg):
        if not msg.topic in self.subscribers:
            return
        for sub in self.subscribers[msg.topic]:
            sub(json.loads(msg.payload))

    def publish(self, topic, message):
        self.client.publish(topic, json.dumps(message))