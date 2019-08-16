import os
import importlib
import logging
from flask import request
logger = logging.getLogger('endpoint')

def load(webApp, dbClient, mqClient):
    enames = os.listdir('web/endpoints')
    for ename in enames:
        if ename in ['__init__.py', '__init__.pyc']:
            continue
        ename_parts = os.path.basename(ename).split('.')
        if ename_parts[1] != 'py':
            continue
        logger.info('loading endpoint %s', ename_parts[0])
        try:
            module = importlib.import_module('endpoints.' + ename_parts[0])
            Endpoint(webApp, dbClient, mqClient, module)
        except Exception as e:
            logger.error('error loading: %s', str(e))

class Endpoint:
    def __init__(self, webApp, dbClient, mqClient, module):
        url = module.url
        methods = module.methods
        handler = module.handle

        module.init(dbClient, mqClient, logger)
        
        logger.debug('url: %s', url)
        logger.debug('methods: %s', methods)
        @webApp.route(url, methods=methods, endpoint=module.name)
        def handle(*args,**kwargs):
            logger.debug('path data: %s', kwargs)
            logger.debug('request data: %s', request)
            return handler(kwargs, request)