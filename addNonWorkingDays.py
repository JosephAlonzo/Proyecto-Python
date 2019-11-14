import tkinter as tk
from tkinter import ttk
import json
import datetime
import time
from datetime import date,timedelta

from tkinter import messagebox
from Clases.calendarioExamenes import CalendarioExamenes
from Clases.jsonConverter import jsonConverter
from tkcalendar import Calendar, DateEntry


class SubWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.json = jsonConverter()
        self.title("Generar Excel")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        # Change what happens when you click the X button
        # This is done so changes also reflect in the main window class
        self.protocol('WM_DELETE_WINDOW', master.close)
        self.txt = ttk.Entry(self)
        self.txt.grid(column = 1, row = 0)
        self.btn = ttk.Button(self, text='Guardar', command= lambda: self.saveDate() )
        self.btn.grid(column=2, row=0)
        self.txt.bind("<Button-1>", self.tkinterCalendar)

        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11)) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13,'bold')) # Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders
        self.treeView = ttk.Treeview(self, style="mystyle.Treeview")
        self.treeView.grid(columnspan=3)

        self.treeView["columns"] = ["Fecha","Eliminar"]
        self.treeView["show"] = "headings"

        self.treeView.column("Fecha",anchor=tk.CENTER)
        self.treeView.column("Eliminar",anchor=tk.CENTER)

        self.treeView.heading("Fecha", text="Fecha",anchor=tk.CENTER)
        self.treeView.heading("Eliminar", text="",anchor=tk.W)

        self.treeView.heading("Fecha", text="Fecha")
        self.treeView.grid(column=0, row=2,sticky="nsew")
        self.fillTable()
        self.treeView.bind('<ButtonRelease-1>', self.selected_item)

        master.grid(sticky="nsew")

        now = datetime.datetime.now()
        self.dia =now.day
        self.mes =now.month
        self.anio =now.year

    def tkinterCalendar(self,event):
        def print_sel():
            f = (cal.selection_get()).weekday()
            if f < 5:
                print(cal.selection_get())
                event.widget.config(state="normal")
                self.updateDate(cal.selection_get())
                event.widget.delete(0, tk.END)
                event.widget.insert(0, cal.selection_get())
                event.widget.config(state="disabled")
                top.destroy()
            else:
                tk.messagebox.showerror(parent=top, message="Por favor elija un dia valido", title="Seleccionar fecha")
    
        top = tk.Toplevel(self)
        cal = Calendar(top,
                    font="Arial 14", selectmode='day',
                    cursor="hand1", year=self.anio, month=self.mes, day=self.dia)
        cal.pack(fill="both", expand=True)
        ttk.Button(top, text="ok", command=print_sel).pack()

    def updateDate(self, date):
        self.dia =  date.day
        self.mes =  date.month
        self.anio = date.year
        
    def selected_item(self, event):
        curItem = self.treeView.item(self.treeView.focus())
        col = self.treeView.identify_column(event.x)
        if col == '#2':
            respuesta = tk.messagebox.askquestion(parent=self, message="¿Esta seguro de desear eliminar el día inhábil: {}?".format(curItem['values'][0]), title="Eliminar registro",icon = 'warning')
            if respuesta == 'yes':
                fecha = curItem['values'][0].split("/")
                fecha = '{}-{}-{}'.format(fecha[2],fecha[1],fecha[0])
                if self.json.deleteFechaJson(fecha):
                    tk.messagebox.showinfo(parent=self, message="Se ha eliminado el día inhábil", title="Eliminar día inhábil")
                    self.fillTable()
                else:
                    tk.messagebox.showerror(parent=self, message="No se pudo completar la acción", title="Eliminar día inhábil")

    def fillTable(self):
        #Limpiar treeview
        self.treeView.delete(*self.treeView.get_children())
        try:
            with open('./data.json') as file:
                data = json.load(file)
                data['Fecha'].sort(key=lambda x: time.mktime(time.strptime(x,"%Y-%m-%d")))
                for item in data['Fecha']:
                    item = item.split('-')
                    item = '{}/{}/{}'.format(item[2], item[1], item[0])
                    self.treeView.insert("", 'end',values=( item, "Eliminar") )
        except:
            pass
        self.txt.delete(0, tk.END)

    def saveDate(self):
        fecha = self.txt.get()
        if fecha != '':
            if self.json.saveFecha(self,fecha):
                tk.messagebox.showinfo(parent=self, message="Se ha guardado la fecha", title="Guardar fecha")
                self.fillTable()
            else:
                tk.messagebox.showwarning(parent=self, message="No se pudo completar la acción ", title="Guardar fecha")
        else: 
            tk.messagebox.showwarning(parent=self, message="Seleccione una fecha", title="Guardar fecha")
