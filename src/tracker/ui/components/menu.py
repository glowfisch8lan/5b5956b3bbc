import tkinter as tk
from tkinter import ttk


class MenuComponent(tk.Frame):
    def __init__(self, ctx, controller):
        super().__init__()

        track_btn = ttk.Button(ctx, text="Back", command=lambda: controller.back_main())
        track_btn.grid(row=1, column=1, padx=10, pady=10)
