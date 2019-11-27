#   *************************************                                 
#   **                                 **
#   **       autor: Alonzo joseph      **
#   **        fecha: 18/11/2019        **
#   **               UTM               **
#   **                                 **
#   *************************************
from tkcalendar import Calendar, DateEntry
from openpyxl import load_workbook
import datetime
from datetime import date,timedelta

class excelCreator():
    def __init__(self, calendarios, grupo, fechas, calendarioGrupo):
        self.calendarios = calendarios
        self.grupo = grupo
        self.fechas = fechas
        self.Celdas = ['A','B','C','D','E','F','G']
        self.calendarioGrupo = calendarioGrupo

    def createExcel(self):
        archivo = load_workbook('template.xlsx')
        # leer y prepara para escribir
        datosTemplate = archivo.active
        
        # Celdas para llenar datos
        datosTemplate['B2'] = self.grupo #la columna de grado y grupo
        datosTemplate['B3'] = 'TIC-ITI Sep-Dic 2019' # Carrera y periodo sep-dic,etc..

        datosTemplate = self.add_dates(datosTemplate)
        listaMaterias = self.get_list_materias()
        datosTemplate = self.add_lista_materias(listaMaterias,datosTemplate)
        # Formato final para guardar
        archivo.save("calendario.xlsx")



    def date_format(self, fecha):
        dia = int(fecha[2])
        mes = int(fecha[1])
        anio = int(fecha[0])
        fecha = date(anio, mes, dia)

        months = ("Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic")
        day = fecha.day
        month = months[fecha.month - 1]
        formato = "{}-{}".format(day, month)
        return formato

    def date_format_asignatura(self, fecha):
        dias = ['Lunes','Martes','Miercoles','Jueves','Viernes']
        months = ("Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")
        f = fecha.weekday()
        f = dias[f]
        day = fecha.day
        month = months[fecha.month - 1]
        formato = "{} {} de {}".format(f, day, month)
        return formato

    def add_dates(self, datosTemplate):
        for i in range(len(self.Celdas)-1):
            try:
                fecha = self.date_format(self.fechas[i])
            except:
                fecha = self.fechas[i]
            datosTemplate[self.Celdas[i+1]+'8'] = fecha
        return datosTemplate

    def add_lista_materias(self, lista, datosTemplate):
        index = 9
        encontrado = False
        self.Celdas = ['B','C','D','E','F','G']
        for x in range(len(lista)):
            materia = lista[x]
            datosTemplate['A' + str(index+x)] = materia
            for periodo in range(len(self.Celdas)):
                if self.calendarios[periodo] == 'Pendiente':
                    celda = self.Celdas[periodo] + str(index+x)
                    datosTemplate[celda] = 'Pendiente'
                    continue
                if materia[0:6].lower() == 'inglés' or materia[0:6].lower() == 'ingles':
                    celda = self.Celdas[periodo] + str(index+x)
                    datosTemplate[celda] = 'De acuerdo a la coordinación de inglés'
                    continue
                calendarioPeriodo = self.calendarios[periodo] 
                for calendario in range(len(calendarioPeriodo)):
                    if encontrado == True:
                        break
                    arrayRow = self.calendarios[periodo][calendario]
                    for row in range(len(arrayRow)):
                        if encontrado == True:
                            break
                        arrayColumn = self.calendarios[periodo][calendario][row]
                        for column in range(len( arrayColumn )):
                            if column == 0:
                                continue
                            info = self.calendarios[periodo][calendario][row][column]
                            try:
                                clase = info['materia']
                            except:
                                clase = ''

                            if clase == materia:
                                fecha = self.date_format_asignatura(info['fecha'])
                                salon = info['salon']
                                hora = arrayColumn[0].split('-')
                                hora = hora[0]
                                texto = '{} \n {} - {}'.format(fecha, salon, hora)
                                celda = self.Celdas[periodo] + str(index+x)
                                datosTemplate[celda] = texto
                                encontrado = True
                                break
                encontrado = False
        
        return datosTemplate
    
   
    def get_list_materias(self):
        calendario = ''
        index = 0
        listaMaterias = []
        while calendario == '' or calendario == 'Pendiente':
            calendario = self.calendarios[index]
            index += 1
        for z in range(len(calendario)):
            for i in range(len(calendario[z])):
                if i == 0:
                    continue
                for j in range(len(calendario[z][i])):
                    if j == 0:
                        continue
                    if calendario[z][i][j] == 'inhabil':
                        calendario[z][i][j] = ''

        for z in range(len(calendario)):
            for i in range(len(calendario[z])):
                if i == 0:
                    continue
                for j in range(len(calendario[z][i])):
                    if j == 0:
                        continue
                    if calendario[z][i][j] != '':
                        listaMaterias.append(
                            calendario[z][i][j]['materia']
                        )
        listaMaterias.append(
            self.get_ingles_name()
        )
        return listaMaterias

    def get_ingles_name(self):
        ingles = ''
        for row in self.calendarioGrupo:
            for column in row:
                try:
                    comparacion = column['materia'][0:6].lower()
                    if comparacion == 'ingles' or comparacion == 'inglés':
                        ingles = column['materia']
                        break
                except:
                    continue
        return ingles