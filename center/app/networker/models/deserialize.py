from importlib import import_module

def deserializeObject(key, descriptor, obj_data):
    if not obj_data:
        return None
    return Model(descriptor['schema'], data=obj_data)

def deserializeClass(key, descriptor, cls_data):
    if not cls_data:
        return None
    module = import_module('entities.' + descriptor['module'])
    ctor = module.__getattribute__(descriptor['class'])
    return ctor(cls_data)

def deserializeSingle(key, descriptor, data):
    field_type = descriptor.get('type', 'primitive')
    field_def = descriptor.get('default', None)
    data = data.get(key, field_def)
    if field_type == 'primitive':
        return data
    elif field_type == 'object':
        return deserializeObject(key, descriptor, data)
    elif field_type == 'class':
        return deserializeClass(key, descriptor, data)

def deserializeArray(key, descriptor, data):
    field_type = descriptor.get('type', 'primitive')
    array = data.get(key, [])
    if field_type == 'primitive':
        return array
    elif field_type == 'object':
        return [deserializeObject(key, descriptor, item)
                                for item in array]
    elif field_type == 'class':
        return [deserializeClass(key, descriptor, item)
                                for item in array]

def deserializeField(key, descriptor, data):
    # logger.debug('deserialize field: %s, %s, %s', key, descriptor, data)
    field_mult = descriptor.get('mult', 'single')
    if field_mult == 'single':
        return deserializeSingle(key, descriptor, data)
    else:
        return deserializeArray(key, descriptor, data)