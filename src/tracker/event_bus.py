listeners = {}


def add_listener(event, listener):
    l = listeners.get(event, None)
    if l is None:
        listeners.setdefault(event, [])

    listeners[event].append(listener)


def dispatch(event, payload=None):
    l = listeners.get(event, None)
    if l is None:
        pass
    for listener in l:
        listener(payload)
