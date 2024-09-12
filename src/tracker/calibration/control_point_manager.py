import time
from typing import List

from src.tracker import event_bus
from src.tracker.calibration.dtos.created_calibration_point_dto import CreatedCalibrationPointDto
from src.tracker.events import CREATED_CALIBRATION_POINT
from src.tracker.landmarkers import landmarker_bus
from mediapipe.tasks.python.components.containers import NormalizedLandmark


# https://storage.googleapis.com/mediapipe-assets/documentation/mediapipe_face_landmark_fullsize.png
# IRIS POINT LEFT - 468
# IRIS POINT RIGHT - 473
def created_calibration_point_listener(payload: CreatedCalibrationPointDto):
    if len(payload.face.face_landmarks) > 0:
        normalized_points = payload.face.face_landmarks.pop()
        left_iris: NormalizedLandmark = normalized_points[468]
        right_iris: NormalizedLandmark = normalized_points[473]
        print(f'{left_iris.x} - {left_iris.y}, {right_iris.x} - {right_iris.y}')
    pass


event_bus.add_listener(CREATED_CALIBRATION_POINT, created_calibration_point_listener)


def write_control_point():
    event_bus.dispatch(CREATED_CALIBRATION_POINT,
                       payload=CreatedCalibrationPointDto(face=landmarker_bus.get('face'), timestamp=time.time()))
