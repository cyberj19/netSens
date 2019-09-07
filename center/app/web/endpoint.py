import os
import importlib
import logging
from flask import request
import mlog
logger = logging.getLogger('endpoint')

def getPackageFiles(dir):
    enames = os.listdir(dir)
    for ename in enames:
        if ename in ['__init__.py', '__init__.pyc']:
            continue
        ename_parts = os.path.basename(ename).split('.')
        if len(ename_parts) > 1 and ename_parts[1] != 'py':
            continue
        yield ename_parts[0]


def load(webApp, dbClient, mqClient, env):
    for ename in getPackageFiles('web/endpoints'):
        logger.info('loading endpoint %s', ename)
        try:
            module = importlib.import_module('endpoints.' + ename)
            mlog.configLoggers([module.name], env.logs_folder, env.debug_mode)
            Endpoint(webApp, dbClient, mqClient, logger, module)
        except Exception as e:
            logger.error('error loading: %s', str(e))

class Endpoint:
    def __init__(self, webApp, dbClient, mqClient, logger, module):
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