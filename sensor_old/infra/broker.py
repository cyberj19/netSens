import threading

class Broker:
    def __init__(self):
        self._listeners = dict()
        self._counters = dict()
        self._countersLock = threading.Lock()
    def on(self, event, callback):
        if not event in self._listeners:
            self._listeners[event] = list()
        self._listeners[event].append(callback)
    
    def emit(self, event, data=None):
        if not event in self._listeners:
            return
        for listener in self._listeners[event]:
            listener(data)

    def getId(self, counterName):
        with self._countersLock:
            if not counterName in self._counters:
                self._counters[counterName] = {
                    'val': 0,
                    'lock': threading.Lock()
                }
        with self._counters[counterName]['lock']:
            id = self._counters[counterName]['val']
            self._counters[counterName]['val'] += 1
        return id