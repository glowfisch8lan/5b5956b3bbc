import tkinter as tk
from tkinter import ttk

from src.tracker.ui.calibration.w_camera_face import WCameraFaceThread
from src.tracker.ui.calibration.w_camera_front import WCameraFrontThread
from src.tracker.ui.calibration.w_controls import WControlsThread
from src.tracker.ui.const import LARGEFONT


class CalibrationPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.w_camera_front = None
        self.w_settings = None
        self.window = None
        self.controller = controller
        self.threads = []

        label = ttk.Label(self, text="Calibrate", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)
        track_btn = ttk.Button(self, text="Back", command=lambda: self.back())
        track_btn.grid(row=1, column=1, padx=10, pady=10)
        track_btn = ttk.Button(self, text="Run", command=lambda: self.do())
        track_btn.grid(row=1, column=2, padx=10, pady=10)

    def destroy(self):
        print('CalibrationPage.destroy')
        self.destroy_window()
        self._destroy_threads()

    def destroy_window(self):
        if self.window:
            self.window.destroy()

    def _destroy_threads(self):
        for thread in self.threads:
            thread.stop()

    def back(self):
        self.controller.back_main()

    def do(self):
        self._destroy_threads()
        self._open_front_camera()
        self._open_face_camera()
        self._open_controls()

    def _open_controls(self):
        thread = WControlsThread()
        self.threads.append(thread)
        thread.start()

    def _open_front_camera(self):
        thread = WCameraFrontThread()
        self.threads.append(thread)
        thread.start()

    def _open_face_camera(self):
        thread = WCameraFaceThread()
        self.threads.append(thread)
        thread.start()
