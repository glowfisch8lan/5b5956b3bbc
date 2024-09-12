import threading
import tkinter as tk

import PIL.Image
import PIL.ImageTk
import cv2
import numpy as np

from src.tracker.landmarkers.face_landmarker import LandmarkDetector

hsv_min = np.array((65, 126, 98), np.uint8)
hsv_max = np.array((96, 255, 255), np.uint8)
color_yellow = (0, 255, 255)


class WCameraFaceThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(WCameraFaceThread, self).__init__(*args, **kwargs)
        self.obj = None
        self._stop = threading.Event()

    def stop(self):
        self.obj.destroy()
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        if self.stopped():
            return
        self.obj = WCameraFace()


class WCameraFace:
    def __init__(self):
        try:
            self.window = tk.Toplevel()
            self.window.title("Calibration Face")  # Rename this
            self.vid = None
            self.is_running = True
            self.landmark_detector = None

            self.label_widget = tk.Label(self.window)
            self.label_widget.pack()

            self._landmark_detector_create()
            self._connect_camera()
            self._show()

        except Exception:
            return

    def destroy(self):
        print('WCameraFace.destroy')
        self.is_running = False
        if self.vid is not None:
            self.vid.release()
        if self.window is not None:
            self.window.destroy()

    def _update(self):
        if self.is_running:
            self.window.after(10, self._show)

    def _show(self):
        _, frame = self.vid.read()
        frame = cv2.flip(frame, 1)
        self.landmark_detector.detect_async(frame)

        frame = self.landmark_detector.draw_landmarks_on_image(frame)

        opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        captured_image = PIL.Image.fromarray(opencv_image)
        photo_image = PIL.ImageTk.PhotoImage(image=captured_image)
        self.label_widget.photo_image = photo_image
        self.label_widget.configure(image=photo_image)
        self._update()

    def _landmark_detector_create(self):
        self.landmark_detector = LandmarkDetector()

    def _connect_camera(self):
        self.vid = cv2.VideoCapture(0)
