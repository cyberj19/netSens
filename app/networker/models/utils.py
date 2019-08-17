import re
def camel2snake(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return 's_' + re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def snake2camel(name):
    components = name.split('_')
    return components[1] + ''.join(x.title() for x in components[2:])
