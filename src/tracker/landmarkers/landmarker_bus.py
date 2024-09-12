landmarkers = {}


def add(landmarker, payload):
    landmarkers[landmarker] = payload


def get(landmarker):
    return landmarkers.get(landmarker, None)
