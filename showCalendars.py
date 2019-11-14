import tkinter as tk
from tkinter import ttk

from tkinter import messagebox

class SubWindow(tk.Toplevel):
    def __init__(self, master, *argv):
        super().__init__(master)
        self.title("Calendario")
        self.calendarios = argv
        # Change what happens when you click the X button
        # This is done so changes also reflect in the main window class
        self.protocol('WM_DELETE_WINDOW', master.close)

    