import os
import importlib
import logging
logger = logging.getLogger('parser')
logger.info('loading parsers')
parsers = []
path = os.path.dirname(__file__)
for module_file in os.listdir(os.path.dirname(__file__)):
    if module_file == '__init__.py' or module_file == 'utils.py' or module_file[-3:] != '.py':
        continue
    print 'importing parser: %s' % module_file
    module = importlib.import_module('.' + module_file[:-3], package='parsers')
    print 'loaded parser: %s' % module.name
    parsers.append(module.parseFunc)
del module_file, module