import flask
import endpoints
import os

class WebServer:
    def __init__(self, env, db, gtw, broker):
        self.app = flask.Flask('NetSens',
                               static_url_path='/', 
                               static_folder='/web')
        
        port = env.flask_port
        @self.app.route('/', methods=['GET'], defaults={'file':'index.html'})
        @self.app.route('/<file>', methods=['GET'])
        def getFile(file):
            return flask.send_from_directory('web',file)

        @self.app.route('/controllers/<file>', methods=['GET'])
        def getController(file):
            return flask.send_from_directory('web/controllers',file)
        @self.app.route('/templates/<file>', methods=['GET'])
        def getTemplate(file):
            return flask.send_from_directory('web/templates',file)

        blueprint = endpoints.create_blue_print(env, broker, db, gtw)
        self.app.register_blueprint(blueprint)
        self.port = port
        self.app.run(host='0.0.0.0', port=self.port)