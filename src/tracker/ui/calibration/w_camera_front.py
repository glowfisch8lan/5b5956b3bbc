import threading
import tkinter as tk

import PIL.Image
import PIL.ImageTk
import cv2
import numpy as np

from settings import ROOT_DIR

hsv_min = np.array((65, 126, 98), np.uint8)
hsv_max = np.array((96, 255, 255), np.uint8)
color_yellow = (0, 255, 255)


class WCameraFrontThread(threading.Thread):
    # Thread class with a _stop() method.
    # The thread itself has to check
    # regularly for the stopped() condition.

    def __init__(self, *args, **kwargs):
        super(WCameraFrontThread, self).__init__(*args, **kwargs)
        self.obj = None
        self._stop = threading.Event()

    # function using _stop function
    def stop(self):
        self.obj.destroy()
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        if self.stopped():
            return
        self.obj = WCameraFront()


class WCameraFront:
    def __init__(self):
        try:
            self.window = tk.Toplevel()
            self.window.title("Calibration Front")  # Rename this
            self.window.geometry("400x400")
            self.vid = None
            self.is_running = True

            self.label_widget = tk.Label(self.window)
            self.label_widget.pack()

            self._connect_camera()
            self._show()

        except Exception:
            return

    def destroy(self):
        print('WCameraFront.destroy')
        self.is_running = False
        if self.window is not None:
            self.window.destroy()

    def _update(self):
        if self.is_running:
            self.window.after(10, self._show)

    def _show(self):
        # _, frame = self.vid.read()
        frame = self.vid
        frame = cv2.resize(frame, [400, 400])

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        thresh = cv2.inRange(hsv, hsv_min, hsv_max)

        moments = cv2.moments(thresh, 1)
        dM01 = moments['m01']
        dM10 = moments['m10']
        dArea = moments['m00']

        if dArea > 100:
            x = int(dM10 / dArea)
            y = int(dM01 / dArea)
            cv2.circle(frame, (x, y), 10, (0, 0, 255), -1)
            cv2.putText(frame, "%d-%d" % (x, y), (x + 10, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color_yellow, 2)

        opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        captured_image = PIL.Image.fromarray(opencv_image)
        photo_image = PIL.ImageTk.PhotoImage(image=captured_image)

        self.label_widget.photo_image = photo_image
        self.label_widget.configure(image=photo_image)

        self._update()

    def _connect_camera(self):
        # self.vid = cv2.VideoCapture(0)
        self.vid = cv2.imread(ROOT_DIR + "/assets/green_cp.jpg")
        # width, height = 800, 600
        # self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        # self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
