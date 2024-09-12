import time

import cv2
import mediapipe as mp

from src.tracker.landmarkers.face_landmarker import LandmarkDetector

def main():
    cap = cv2.VideoCapture(0)
    landmarker = LandmarkDetector()

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        landmarker.detect_async(frame)

        frame = landmarker.draw_landmarks_on_image(frame)

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            break

    landmarker.close()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
