#   *************************************
#   **                                 **
#   **       autor: Alonzo joseph      **
#   **        fecha: 10/11/2019        **
#   **               UTM               **
#   **                                 **
#   *************************************
import json
import tkinter as tk
from tkinter import messagebox

class jsonConverter():
    def __init__(self):
        self.data = {}

    def convertArrayToJSON(self, array, ventana):
        self.array = array
        try:
            name = self.array[0][0].split("-")
            name = name[0]
            try:
                with open('./data.json') as file:
                    self.data = json.load(file)
                if self.validarSiYaExisteElHorarioGuardado(self.data, name):
                        MsgBox = tk.messagebox.askquestion (parent=ventana, title= 'Registro ya guardado',message='Estas seguro de sobrescribir la información guardada',icon = 'warning')
                        if MsgBox == 'no':
                            return False
                        else:
                            pass 
                try:
                    self.data['Calendario'][name] = []
                except:
                    self.data['Calendario']= {}
                    self.data['Calendario'][name] = []
            except:
                return False

            
            dias = ['Lu', 'Ma', 'Mi', 'Ju', 'Vi']
            for x in range( len(self.array) ):
                if x == 0:
                    continue
                for y in range( len(self.array[x]) ):
                    if y == 0:
                        horario = self.array[x][y]
                        continue
                    materia = self.array[x][y]['materia']
                    maestro =  self.array[x][y]['maestro']
                    salon = self.array[x][y]['salon']
                    color =  self.array[x][y]['color']
                    self.data['Calendario'][name].append({
                        'materia': materia,
                        'maestro': maestro,
                        'salon': salon,
                        'color': color,
                        'horario': horario,
                        'dia' : dias[y-1]
                    })
            
            with open('./data.json', 'w') as file:
                json.dump(self.data, file, indent=4)
            return True
        except:
            return False

    def getCalendario(self,ventana, grupo):
        try:
            with open('./data.json') as file:
                self.data = json.load(file)
                self.data = self.changeFormat(self.data['Calendario'][grupo])
                return self.data
        except:
            tk.messagebox.showwarning(parent=ventana,title='Error', message='No se pudo recuperar el horario seleccionado!' )
            pass
    
    def changeFormat(self, array):
        data = []
        clases = []
        horario = array[0]['horario']
        clases.append({
            horario  
        })
        for item in array:
            if horario == item['horario']:
                clases.append({
                    'materia': item['materia'],
                    'maestro': item['maestro'],
                    'salon': item['salon'],
                    'color': item['color']
                })
            else:
                horario = item['horario']
                data.append(clases)
                clases = []
                clases.append({
                    horario  
                })
                clases.append({
                    'materia': item['materia'],
                    'maestro': item['maestro'],
                    'salon': item['salon'],
                    'color': item['color']
                })
        data.append(clases)
        return data


    def deleteItemJson(self, item):
        try:
            try:
                with open('./data.json') as file:
                    self.data = json.load(file)
                    self.data['Calendario'].pop(item)
            except:
                return False   
            with open('./data.json', 'w') as file:
                json.dump(self.data, file, indent=4)
            return True
        except:
            return False

    def validarSiYaExisteElHorarioGuardado(self, array, grupo):
        for x in array['Calendario']:
            if x.upper() == grupo.upper():
                return True
        return False

    def saveFecha(self,ventana, fecha):
        try:
            with open('./data.json') as file:
                self.data = json.load(file)
            if self.validarSiYaExisteFechaGuardada(self.data, fecha):
                tk.messagebox.showinfo(parent=ventana, title='Registro ya guardado', message='La fecha indicada ya ha sido guardada con anterioridad',icon = 'warning' )
                return False
        except:
            self.data['Fecha']= []

        self.data['Fecha'].append(fecha)

        with open('./data.json', 'w') as file:
            json.dump(self.data, file, indent=4)
            return True

    def validarSiYaExisteFechaGuardada(self, array,fecha ):
        for x in array['Fecha']:
            if x == fecha:
                return True
        return False

    def getFechas(self, ventana):
        try:
            with open('./data.json') as file:
                self.data = json.load(file)
                return self.data['Fecha']
        except:
            tk.messagebox.showwarning(parent=ventana,title='Error', message='No se pudo recuperar la información solicitada!' )
            pass

    def deleteFechaJson(self, fecha):
        try:
            try:
                with open('./data.json') as file:
                    self.data = json.load(file)
                    self.data['Fecha'].remove(fecha)
            except:
                return False   
            with open('./data.json', 'w') as file:
                json.dump(self.data, file, indent=4)
            return True
        except:
            return False