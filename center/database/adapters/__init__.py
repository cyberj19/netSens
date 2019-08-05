def getAdapter(env):
    if env.db_type == 'mongo':
		import mongoadapter
		return mongoadapter.MongoDBAdapter(env)
    elif env.db_type == 'tinydb':
		import tinydbadapter
		return tinydbadapter.TinyDBAdapter(env)
    elif env.db_type == 'json':
		import jsonadapter
		return jsonadapter.JsonAdapter(env)
    else:
        raise Exception('Unknown db type: %s' % env.db_type)