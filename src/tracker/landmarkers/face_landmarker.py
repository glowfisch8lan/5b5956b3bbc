import os
import time

import mediapipe as mp
import numpy as np
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2

from src.tracker.landmarkers import landmarker_bus


class LandmarkDetector:
    def __init__(self):
        self.result = mp.tasks.vision.FaceLandmarkerResult
        self.landmarker = mp.tasks.vision.FaceLandmarker
        self.create()

    def update_result(self, result: mp.tasks.vision.FaceLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
        landmarker_bus.add('face', result)
        self.result = result

    def create(self):
        options = mp.tasks.vision.FaceLandmarkerOptions(
            base_options=mp.tasks.BaseOptions(
                model_asset_path=os.path.dirname(os.path.realpath(__file__)) + '/models/face_landmarker.task'),
            running_mode=mp.tasks.vision.RunningMode.LIVE_STREAM,
            result_callback=self.update_result)

        self.landmarker = self.landmarker.create_from_options(options)

    def detect_async(self, frame):
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        self.landmarker.detect_async(image=mp_image, timestamp_ms=int(time.time() * 1000))

    def close(self):
        self.landmarker.close()

    def draw_landmarks_on_image(self, rgb_image):
        try:
            if not self.result.face_landmarks:
                return rgb_image
            else:
                face_landmarks_list = self.result.face_landmarks
                annotated_image = np.copy(rgb_image)

                # Loop through the detected faces to visualize.
                for idx in range(len(face_landmarks_list)):
                    face_landmarks = face_landmarks_list[idx]

                    # Draw the face landmarks.
                    face_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
                    face_landmarks_proto.landmark.extend([
                        landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in
                        face_landmarks
                    ])

                    # solutions.drawing_utils.draw_landmarks(
                    #     image=annotated_image,
                    #     landmark_list=face_landmarks_proto,
                    #     connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
                    #     landmark_drawing_spec=None,
                    #     connection_drawing_spec=mp.solutions.drawing_styles
                    #     .get_default_face_mesh_tesselation_style())

                    solutions.drawing_utils.draw_landmarks(
                        image=annotated_image,
                        landmark_list=face_landmarks_proto,
                        connections=mp.solutions.face_mesh.FACEMESH_CONTOURS,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp.solutions.drawing_styles
                        .get_default_face_mesh_contours_style())

                    solutions.drawing_utils.draw_landmarks(
                        image=annotated_image,
                        landmark_list=face_landmarks_proto,
                        connections=mp.solutions.face_mesh.FACEMESH_IRISES,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp.solutions.drawing_styles
                        .get_default_face_mesh_iris_connections_style())

                return annotated_image
        except:
            return rgb_image
