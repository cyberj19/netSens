import threading
import logging
import paho.mqtt.client as mqtt
import json
logger = logging.getLogger('mqtt')

class MQTTClient:
    def __init__(self, env):
        self.host = env.mqtt_host
        self.port = env.mqtt_port
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.connect(self.host, self.port, 60)
        threading.Thread(target=self.client.loop_forever).start()

    def on_connect(self, client, userdata, flags, rc):
        logger.info("Connected with result code %s", str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        # client.subscribe("$SYS/#")

    def on_message(self, client, userdata, msg):
        pass
        # logger.debug('%s: %s', msg.topic, str(msg.payload))
    
    def publish(self, topic, message):
        self.client.publish(topic, json.dumps(message))