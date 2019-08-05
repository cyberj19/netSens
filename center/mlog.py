import logging
import time
import env
import os

def createLogger(name):
    logger = logging.getLogger(name)
    filename = '%s/%s_%d' % (env.logs_folder,name.lower(),time.time())
    if not os.path.exists(env.logs_folder):
        os.makedirs(env.logs_folder)
    if not os.path.exists(env.stdout_log_dir):
	os.makedirs(env.stdout_log_dir)
    debugFormatter = logging.Formatter(
            '%(asctime)s %(name)-12s {%(filename)s:%(lineno)d} %(levelname)-8s %(message)s'

    )
    infoFormatter = logging.Formatter(
            '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')


    handler = logging.FileHandler(filename)
    handler.setFormatter(debugFormatter)
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    shandler = logging.StreamHandler()
    if env.debug_mode:
        shandler.setFormatter(debugFormatter)
        shandler.setLevel(logging.DEBUG)
    else:
        shandler.setFormatter(infoFormatter)
        shandler.setLevel(logging.INFO)
        
    logger.addHandler(shandler)

    logger.setLevel(logging.DEBUG)


logs = ['db','processor','main','gtw','web', 'api']

for log in logs:
    createLogger(log)

logging.getLogger('main').info('Logs created')
