import tkinter as tk
from tkinter import ttk

from src.tracker.ui.components.menu import MenuComponent
from src.tracker.ui.const import LARGEFONT


class TrackPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = ttk.Label(self, text="Track", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)
        MenuComponent(self, self.controller)

    def destroy(self):
        print('TrackPage.destroy')