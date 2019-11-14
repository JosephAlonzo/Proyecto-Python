import tkinter as tk
from tkinter import ttk

from tkinter import messagebox
from Clases.calendario import Calendario
from Clases.htmlRecuperator import HtmlRecuperator
from Clases.jsonConverter import jsonConverter
import time
import threading
from tkinter.ttk import Progressbar

class SubWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Agregar Horario por link")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=5)
        self.rowconfigure(1, weight=3)
        
        # Change what happens when you click the X button
        # This is done so changes also reflect in the main window class
        self.protocol('WM_DELETE_WINDOW', master.close)


        self.label = tk.Label(self, text="Link")
        self.label.grid(column=0, row=0,padx=30, pady=30)

        self.content = tk.StringVar()
        self.txt = tk.Entry(self, width=30, textvariable=self.content)
        self.txt.grid(column=1, row = 0)
        self.labelsArray = []
        self.btn =  ttk.Button(self, text="Enviar", command= lambda: self.saveJson() )
        self.btn.grid(column = 2, row=0, columnspan=2,sticky="nsew",padx=30, pady=30, ipadx=5, ipady=5)
        self.progress = ttk.Progressbar(self, orient=tk.HORIZONTAL,length=100,  mode='indeterminate')
        

        
    def saveJson(self):
        def real_traitement():
            self.progress.grid(row=1,column=0,columnspan=4, sticky="nsew")
            self.progress.start()
            
            url = self.content.get()
            htmlRecuperator = HtmlRecuperator(url, self)
            svg = htmlRecuperator.getSvg()
            if svg != '':
                calendarioUtm = Calendario()
                calendarioUtm = calendarioUtm.crearCalendario(svg)
                json = jsonConverter()
                respuesta = json.convertArrayToJSON(calendarioUtm, self)

                if respuesta:
                    tk.messagebox.showinfo(parent=self, message="Se ha registrado el horario con exito", title="Registro de horario")
                else:
                    tk.messagebox.showwarning(parent=self, message="No se ha podido completar la acción", title="Registro de horario")
                self.content.set('')

            self.progress.stop()
            self.progress.grid_forget()
            
        threading.Thread(target=real_traitement).start()
