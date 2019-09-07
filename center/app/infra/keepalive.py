import time
def start(mqtt, component, rate=10):
    while True:
        beat(mqtt, component)
        time.sleep(rate)

def beat(mqtt, component):
    mqtt.publish('keepalive', {
        'component': component,
        'time': time.time()
    })