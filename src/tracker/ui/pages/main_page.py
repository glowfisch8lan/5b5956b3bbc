import tkinter as tk
from tkinter import ttk

from src.tracker.ui.const import LARGEFONT
from src.tracker.ui.pages.calibration_page import CalibrationPage
from src.tracker.ui.pages.settings_page import SettingsPage
from src.tracker.ui.pages.track_page import TrackPage


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = ttk.Label(self, text="EYE Tracker", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        track_btn = ttk.Button(self, text="Track", command=lambda: self.controller.show_frame(TrackPage))
        calibrate_btn = ttk.Button(self, text="Calibrate",
                                   command=lambda: self.controller.show_frame(CalibrationPage))
        settings_btn = ttk.Button(self, text="Settings", command=lambda: self.controller.show_frame(SettingsPage))
        quit_btn = ttk.Button(self, text='Quit', command=self.controller.destroy)

        track_btn.grid(row=1, column=1, padx=10, pady=10)
        calibrate_btn.grid(row=1, column=2, padx=10, pady=10)
        settings_btn.grid(row=1, column=3, padx=10, pady=10)
        quit_btn.grid(row=1, column=4, padx=10, pady=10)

    def destroy(self):
        print('MainPage.destroy')
