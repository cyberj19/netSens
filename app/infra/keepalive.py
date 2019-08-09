import time
def start(mqtt, component, rate=10):
    while True:
        mqtt.publish('keepalive', {
            'component': component,
            'time': time.time()
        })
        time.sleep(rate)