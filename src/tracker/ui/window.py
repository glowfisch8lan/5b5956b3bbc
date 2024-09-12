import tkinter as tk

from src.tracker.ui.pages.calibration_page import CalibrationPage
from src.tracker.ui.pages.main_page import MainPage
from src.tracker.ui.pages.settings_page import SettingsPage
from src.tracker.ui.pages.track_page import TrackPage

# TODO делать destroy при возврате назад

class Window(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.routes = None
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.build()

        self.show_frame(MainPage)

    def build(self):
        self.routes = None
        self.routes = (MainPage, SettingsPage, CalibrationPage, TrackPage)

        for F in self.routes:
            frame = F(self.container, self)
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

    def rebuild(self):
        for F in self.routes:
            self.frames[F].destroy()
        self.build()

    def back_main(self):
        frame = self.frames[MainPage]
        self.rebuild()
        frame.tkraise()

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
