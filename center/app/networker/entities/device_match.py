MATCH_IMPOSSIBLE = 0
MATCH_POSSIBLE = 1
MATCH_CERTAIN = 2

match_rules = [
    {
        'properties': ['mac'],
        'score': MATCH_CERTAIN
    },
    {
        'properties': ['ip', 'hostname'],
        'score': MATCH_CERTAIN
    },
    {
        'properties': ['ip'],
        'score': MATCH_POSSIBLE
    },
    {
        'properties': ['hostname'],
        'score': MATCH_POSSIBLE
    }
]

def matchDevices(core1, core2):
    matches = []
    for prop in ['mac', 'ip', 'hostname']:
        p1 = core1[prop]
        p2 = core2[prop]
        if p2:
            if p2 == p1:
                matches.append(prop)
            else:
                matches.append('!' + prop)
    
    best_score = MATCH_IMPOSSIBLE
    for rule in match_rules:
        if set(rule['properties']).issubset(set(matches)):
            if rule['score'] > best_score:
                best_score = rule['score']
    return best_score