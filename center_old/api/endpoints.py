import json
import logging
from flask import Blueprint, request, send_from_directory, render_template, abort
import os

logger = logging.getLogger('api')

def create_blue_print(broker, db, gtw):
    app = Blueprint('netSens_api', __name__)

    @app.route('/api/overview', methods=['GET'])
    def getOverview():
        networks = db.getNetworks(detailed=False)
        listeners = db.getListeners()
        return json.dumps({
            'success': True,
            'networks': networks,
            'listeners': listeners
            })
        
    @app.route('/api/networks/<netId>', methods=['GET'])
    def getNetwork(netId):
        netId = int(netId)
        return json.dumps({
            'success': True,
            'network': db.getNetworkById(netId)
        })

    @app.route('/api/networks/<netId>/clear', methods=['POST'])
    def clearNetwork(netId):
        broker.emit(
            'manualOper',
            {
                'type': 'clearNetwork',
                'networkId': int(netId)
            }
        )
        return json.dumps({'success': True}), 200
    
    @app.route('/api/networks/<netId>/devices/<devId>/fingerBank', methods=['POST'])
    def fingerBank(netId, devId):
        broker.emit(
            'manualOper',
            {
                'type': 'fingerBankRequest',
                'networkId': int(netId),
                'deviceId': int(devId)
            }
        )
        return json.dumps({'success': True}), 200

    @app.route('/api/networks/<netId>/devices/<devId>/macVendors', methods=['POST'])
    def macVendors(netId, devId):
        broker.emit(
            'manualOper',
            {
                'type': 'macVendorsRequest',
                'networkId': int(netId),
                'deviceId': int(devId)
            }
        )
        return json.dumps({'success': True}), 200
    
    @app.route('/api/networks/<netId>/devices/<devId>/comment', methods=['POST'])
    def commentDevice(netId, devId):
        data = request.get_json()
        broker.emit(
            'manualOper',
            {
                'type': 'deviceComment',
                'networkId': int(netId),
                'deviceId': int(devId),
                'comment': data['comment']
            }
        )
        return json.dumps({'success': True}), 200

    @app.route('/api/networks/<netId>/devices/<devId>/close', methods=['POST'])
    def closeDevice(netId, devId):
        broker.emit(
            'manualOper', 
            {
                'type': 'deviceClose', 
                'networkId': int(netId),
                'deviceId': int(devId)
            }
        )
        return json.dumps({'success': True}), 200
    # @app.route('/api/session/device/<devId>/analyze', methods=['GET'])
    # def analyzeDevice(devId):
    #     devId = int(devId)
    #     data = db.getDeviceData(sessionId, devId)
    #     return json.dumps({
    #         'success': True,
    #         'device': data
    #     })

    # @app.route('/api/session/device/<devId>/manualMAC', methods=['POST'])
    # def manualMac(devId):
    #     req = json.loads(request.data)
    #     return json.dumps({'success': True})
		
    @app.route('/api/sensors/<smac>/<intr>/connect', methods=['POST'])
    def connectSensor(smac, intr):
        try:
			gtw.connectInterface(smac, intr)
			return json.dumps({'success':True}), 200
        except Exception, e:
			return json.dumps({'success':False,'error':str(e)})

    @app.route('/api/sensors/<smac>/<intr>/disconnect', methods=['POST'])
    def disconnectSensor(smac, intr):
        try:
			gtw.disconnectInterface(smac, intr)
			return json.dumps({'success':True}), 200
        except Exception, e:
            return json.dumps({'success':False,'error':str(e)})

    return app
