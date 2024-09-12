import tkinter as tk
from tkinter import ttk

from src.tracker.ui.components.menu import MenuComponent
from src.tracker.ui.const import LARGEFONT


class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.do()

    def destroy(self):
        print('SettingsPage.destroy')

    def do(self):
        if __name__ == '__main__':
            label = ttk.Label(self, text="Settings", font=LARGEFONT)
            label.grid(row=0, column=4, padx=10, pady=10)

            MenuComponent(self, self.controller)