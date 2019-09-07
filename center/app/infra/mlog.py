import logging
import time

def configLoggers(names, logs_folder, debug_mode):
	for name in names:
		createLogger(name, logs_folder, debug_mode)
		
def createLogger(name, logs_folder=None, debug_mode=True):
    logger = logging.getLogger(name)

    if logs_folder:
            filename = '%s/%s_%d.log' % (logs_folder,name.lower(),time.time())

    debugFormatter = logging.Formatter(
        '%(asctime)s %(name)-12s {%(filename)s:%(lineno)d} %(levelname)-8s %(message)s'
    )
    infoFormatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')


    if logs_folder:
            handler = logging.FileHandler(filename)
            handler.setFormatter(debugFormatter)
            handler.setLevel(logging.DEBUG)
            logger.addHandler(handler)


    shandler = logging.StreamHandler()
    if debug_mode:
        shandler.setFormatter(debugFormatter)
        shandler.setLevel(logging.DEBUG)
    else:
        shandler.setFormatter(infoFormatter)
        shandler.setLevel(logging.INFO)			
    logger.addHandler(shandler)
	
    logger.setLevel(logging.DEBUG)