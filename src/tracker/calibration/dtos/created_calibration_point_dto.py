from mediapipe.tasks.python.vision.face_landmarker import FaceLandmarkerResult


class CreatedCalibrationPointDto:
    def __init__(self, face: FaceLandmarkerResult, timestamp: float):
        self.face = face
        self.timestamp = timestamp

    def __str__(self):
        return f'{self.timestamp} - {self.face}'
