import logging
import time
import env

def createLoggers(names):
	for name in names:
		createLogger(name)
		
def createLogger(name):
    logger = logging.getLogger(name)
    filename = '%s/%s_%d' % (env.logs_folder,name.lower(),time.time())

    debugFormatter = logging.Formatter(
            '%(asctime)s %(name)-12s {%(filename)s:%(lineno)d} %(levelname)-8s %(message)s'

    )
    infoFormatter = logging.Formatter(
            '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')


    if env.debug_mode:
        handler = logging.FileHandler(filename)
        handler.setFormatter(debugFormatter)
        handler.setLevel(logging.DEBUG)
        logger.addHandler(handler)
        
        shandler = logging.StreamHandler()
        shandler.setFormatter(debugFormatter)
        shandler.setLevel(logging.DEBUG)			
        logger.addHandler(shandler)
        
        logger.setLevel(logging.DEBUG)

def createLoggers(loggerNames):
        for logName in loggerNames:
                createLogger(logName)
