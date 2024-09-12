import threading
import tkinter as tk
from tkinter import ttk
import numpy as np

from src.tracker import event_bus
from src.tracker.calibration import control_point_manager
from src.tracker.events import CREATED_CALIBRATION_POINT
from src.tracker.landmarkers import landmarker_bus

hsv_min = np.array((65, 126, 98), np.uint8)
hsv_max = np.array((96, 255, 255), np.uint8)
color_yellow = (0, 255, 255)


class WControlsThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(WControlsThread, self).__init__(*args, **kwargs)
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
        self.obj = WControls()


class WControls:
    def __init__(self):
        try:
            self.window = tk.Toplevel()
            self.window.title("Calibration Controls")
            self.vid = None
            self.is_running = True
            self.manager = control_point_manager

            track_btn = ttk.Button(self.window, text="Write Point", command=lambda: self.create_point())
            track_btn.grid(row=1, column=2, padx=10, pady=10)

            self._show()

        except Exception:
            return

    def create_point(self):
        self.manager.write_control_point()

    def destroy(self):
        print('WControls.destroy')
        self.is_running = False
        if self.window is not None:
            self.window.destroy()

    def _update(self):
        if self.is_running:
            self.window.after(10, self._show)

    def _show(self):
        self._update()
