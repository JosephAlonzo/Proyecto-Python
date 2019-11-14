import tkinter as tk
from tkinter import ttk
import json

import addCalendar as sW
import createExcel as cE
import addNonWorkingDays as nWD
from tkinter import messagebox
from Clases.jsonConverter import jsonConverter

class Application(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self._second_window = None
        root.columnconfigure(0, weight=2)
        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=6)

        self.btn = ttk.Button(root, text="Agregar nuevo usando link", command= lambda : self.new_window('sW'))
        self.btn.grid(column=2, row=0,sticky="nsew", padx=2, pady=5, ipadx=10, ipady=10)

        self.btn2 = ttk.Button(root, text="Agregar días inhabiles", command= lambda : self.new_window('nWD'))
        self.btn2.grid(column=1, row=0,sticky="nsew", padx=2, pady=5, ipadx=10, ipady=10)

        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11)) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13,'bold')) # Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders
        self.treeView = ttk.Treeview(root, style="mystyle.Treeview")
        self.treeView.grid(columnspan=3)

        self.treeView["columns"] = ["Grupo","Eliminar","GenerarExcel"]
        self.treeView["show"] = "headings"

        self.treeView.column("Grupo",anchor=tk.CENTER)
        self.treeView.column("Eliminar",anchor=tk.CENTER)
        self.treeView.column("GenerarExcel",anchor=tk.CENTER)

        self.treeView.heading("Grupo", text="Grupo",anchor=tk.CENTER)
        self.treeView.heading("Eliminar", text="",anchor=tk.W)
        self.treeView.heading("GenerarExcel", text="",anchor=tk.W)

        self.treeView.heading("Grupo", text="Grupo")
        self.treeView.grid(column=0, row=1,sticky="nsew")
        self.fillTable()
        self.treeView.bind('<ButtonRelease-1>', self.selected_item)
        #Esta madre no sirve
        self.treeView.tag_configure('odd', background='#E8E8E8')
        self.treeView.tag_configure('even', background='#DFDFDF')
        
        self.grid(sticky="nsew")

    def selected_item(self, event):
        curItem = self.treeView.item(self.treeView.focus())
        col = self.treeView.identify_column(event.x)
        #print ('curItem = ', curItem)
        #print ('col = ', col)
        # index = int(col[1:])-1
        # print(index)
        # cell_value = curItem['values'][index]
        # if col == '#0':
        #     cell_value = curItem['text']
        # elif col == '#1':
        #     cell_value = curItem['values'][0]
        if col == '#2':
            respuesta = tk.messagebox.askquestion(message="¿Esta seguro de desear eliminar el calendario del {}?".format(curItem['values'][0]), title="Eliminar registro",icon = 'warning')
            if respuesta == 'yes':
                json = jsonConverter()
                if json.deleteItemJson(curItem['values'][0]):
                    tk.messagebox.showinfo(message="Se ha eliminado el horario con exito", title="Eliminar horario")
                    self.fillTable()
                else:
                    tk.messagebox.showerror(message="No se pudo completar la acción", title="Eliminar horario")

        elif col == '#3':
            respuesta = tk.messagebox.askquestion(message="¿Desea generar el archivo Excel?", title="Generar Excel",icon = 'info')
            json = jsonConverter()
            array =json.getCalendario(self, curItem['values'][0])
            if len(array) > 0 and respuesta == 'yes':
                self.new_window('cE', array,curItem['values'][0] )
            else:
                tk.messagebox.showerror(message="No se pudo completar la acción", title="Generar Excel")

    def fillTable(self):
        #Limpiar treeview
        self.treeView.delete(*self.treeView.get_children())
        try:
            with open('./data.json') as file:
                data = json.load(file)
                for item in data['Calendario']:
                    #self.treeView.insert('', 'end', values=item)
                    self.treeView.insert("", 'end',values=(item, "Eliminar" , "Generar Excel") )
        except:
            pass
    
        
    def new_window(self, ventana, *argv):
        # This prevents multiple clicks opening multiple windows
        if self._second_window is not None:
            return
        if ventana == 'sW':
            self._second_window = sW.SubWindow(self)
        elif ventana == 'cE':
            self._second_window = cE.SubWindow(self,argv)
        elif ventana == 'nWD':
            self._second_window = nWD.SubWindow(self)

    def close(self):
        # Destory the 2nd window and reset the value to None
        if self._second_window is not None:
            self._second_window.destroy()
            self._second_window = None 
            self.fillTable()       
            
            
root = tk.Tk()
app = Application(root)
app.mainloop()

# url = 'https://utm.edupage.org/timetable/view.php?num=18&class=*18'
# htmlRecuperator = htmlRecuperator(url)
# svg = htmlRecuperator.getSvg()

# diasInhabiles = [ '2019,11,1' ]
# fechaFinal = [2019, 11, 6]
# materiasSinExamenes = [ 'tutorias' ]



# calendario = CalendarioExamenes(svg, diasInhabiles, fechaFinal, materiasSinExamenes)
# calendario.crearCalendarioExmanes()
# calendario.printCalendarioExamenes()