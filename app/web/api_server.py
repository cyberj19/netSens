import threading
import logging
import api_endpoints
from flask import Flask

logger = logging.getLogger('api')   
class APIServer:
    def __init__(self, env, mqttClient, dbClient):
        self.port = env.flask_port
        self.app = Flask('netSensWeb')
        bp = api_endpoints.create(env, mqttClient, dbClient)
        self.app.register_blueprint(bp)
        threading.Thread(target=self.listen).start()

    def listen(self):
        self.app.run(host='0.0.0.0', port=self.port)