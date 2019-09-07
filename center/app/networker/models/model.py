from collections import OrderedDict
import re
import importlib
import logging
import time
import uuid
import json
import os
from utils import *
from deserialize import *
logger = logging.getLogger('model')

def generateField(field_gen, time):
    parts = field_gen.split('@')
    if parts[0] == 'time':
        return time
    elif parts[0] == 'uuid':
        return parts[1] + '-' + uuid.uuid4().hex

def createDefaultField(field, presets):
    field_type = field.get('type', 'primitive')
    field_def = field.get('default', None)
    field_pre = field.get('preset', None)
    if field_type == 'primitive':
        if field_pre and field_pre in presets:
            return presets[field_pre]
        elif field_def:
            return field_def
        else:
            return None
    elif field_type == 'class':
        module = importlib.import_module('models.' + field['module'])
        ctor = module.__getattribute__(field['class'])
        return ctor()

class Model(object):
    def __init__(self, schema=None, schema_file=None, data=None, presets=None):
        
        if schema:
            self.schema = schema
        elif schema_file:
            curr_dir = os.path.dirname(os.path.abspath(__file__))
            schema_path = os.path.join(curr_dir, 'schemas', schema_file)
            with open(schema_path, 'r') as fp:
                self.schema = json.load(fp)
        else:
            raise Exception('No schema file supplied')
        self.schema_name = self.schema.get('$name', 'Model')
        if data:
            self.deserialize(data)
        else:
            self.default(presets)

    
    def create_default(self, presets):
        for key in self.schema:
            if key[0] == '$':
                continue
            field = self.schema[key]
            skey = camel2snake(key)
            self.__dict__[skey] = createDefaultField(field, presets)
    
    def deserialize(self, data):
        # logger.debug('deserialize %s, %s', self.schema_name, data)
        if not data:
            return
        for key in self.schema:
            if key[0] == '$':
                continue
            field = self.schema[key]
            skey = camel2snake(key)
            self.__dict__[skey] = deserializeField(key, field, data)

    def __getattr__(self, key):
        # print dir(self.__dict__)
        ckey = 's_' + key
        if ckey in self.__dict__:
            return self.__dict__[ckey]
        return self.__dict__[key]

    def __setattr__(self, key, value):
        ckey = 's_' + key
        if ckey in self.__dict__:
            self.__dict__[ckey] = value
        else:
            self.__dict__[key] = value

    def serialize(self):
        dct = OrderedDict()
        for key in self.schema:
            if key[0] == '$':
                continue
            ckey = camel2snake(key)
            field = self.schema[key]
            field_type = field.get('type', 'primitive')
            field_mult = field.get('mult', 'single')
            data = self.__dict__[ckey]
            if field_mult == 'single':
                if field_type == 'primitive':
                    dct[key] = data
                else:
                    if data:
                        dct[key] = data.serialize()
                    else:
                        dct[key] = None
            else:
                if field_type == 'primitive':
                    dct[key] = data
                else:
                    if data:
                        dct[key] = [a.serialize() for a in data]
                    else:
                        dct[key] = []
        return dct