import tkinter as tk
from tkinter import ttk

from tkinter import messagebox
import datetime
from datetime import date,timedelta
from Clases.excelCreator import excelCreator
import sys
import os

class SubWindow(tk.Toplevel):
    def __init__(self, master, *argv):
        super().__init__(master)
        self.title("Calendarios")
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=10)
        self.rowconfigure(0, weight=1)
        self.frameTitleAndButtons = tk.Frame(self)
        self.frameTitleAndButtons.grid(row=0, column=0, padx=20, pady=20,sticky="nsew")
        self.frameMateriasNoAplicadas = tk.Frame(self)
        self.frameMateriasNoAplicadas.grid(row=0, column=1, padx=20, pady=20,sticky="nsew")
        self.modificacionActivada = False
        self.celdaActivada = []
        self.index = 0
        self.argv = argv
        self.parciales= ['PRIMER PARCIAL', 'SEGUNDO PARCIAL', 'TERCER PARCIAL', 'ORDINARIO 1', 'EXTRAORDINARIO 1', 'EXTRAORDINARIO 2']
        self.fechas = argv[0][4]
        self.listaMateriasNoAplicadas = list(argv[0][5])
        self.protocol('WM_DELETE_WINDOW', master.close)
        self.btn1 = ttk.Button(self.frameTitleAndButtons, text="Anterior",command= lambda: self.lastCalendario(argv))
        self.btn1.grid(row=0, column=1,sticky="w",  pady=10,  ipady=10)
        self.btn2 = ttk.Button(self.frameTitleAndButtons, text="Siguiente",command= lambda: self.nextCalendario(argv))
        self.btn2.grid(row=0, column=2,sticky="w", pady=10, ipady=10)
        if self.index == 0:
            self.btn1.config(
                state="disabled"
            )

        self.listCalendarios = argv[0][0]
        self.calendarioExamenes = self.listCalendarios[self.index] 
        self.grupo = argv[0][3]
        self.dias = [self.grupo, 'Lunes','Martes','Miercoles','Jueves','Viernes']
        self.calendarioGrupo = [self.dias] + argv[0][1]
        self.fechaInicio = argv[0][2][self.index]
        self.fechaFinal = argv[0][4][self.index]
        self.frames = []
        self.btns = []
        self.lbl = ''
        for x in range( len( self.listCalendarios) ):
            if self.listCalendarios[x] == 'Pendiente':
                continue
            for y in range ( len(self.listCalendarios[x])):
                array = self.listCalendarios[x][y]
                self.listCalendarios[x][y] = self.addHorarios(self.calendarioGrupo, array)
        
        if self.calendarioExamenes != 'Pendiente':
            self.printCalendario(self.calendarioExamenes, self.grupo, self.calendarioGrupo, self.fechaInicio)
        else:
            self.printCalendarioPendiente(self.grupo, self.calendarioGrupo)
        self.printListaMateriasNoAplicadas()

    def printListaMateriasNoAplicadas(self):
        try:
            if len(self.listaMateriasNoAplicadas[self.index]) > 0:
                self.btns = [ '' for x in self.listaMateriasNoAplicadas[self.index] ]
                for i in range(len(self.listaMateriasNoAplicadas[self.index])):
                    self.btns[i] = tk.Button(
                            self.frameMateriasNoAplicadas,
                            command= lambda: self.disableMateriaNoAplicada(i),
                            text=self.listaMateriasNoAplicadas[self.index][i],
                            background="#31D68B", 
                            foreground= '#FFFFFF',
                            relief = 'flat')
                    self.btns[i].grid(row=0, column=i,sticky="w", pady=10,  ipady=10)
            else:
                self.frameMateriasNoAplicadas.destroy()
        except:
            self.frameMateriasNoAplicadas.destroy()

    def printCalendario(self, calendarioExamenes, grupo, calendarioGrupo, fechaInicio):
        self.buttons = [ [['' for x in range( len(self.calendarioGrupo[0])  ) ] for j in range( len(self.calendarioGrupo) )] for i in range( len(self.calendarioExamenes) )  ]
        dias = [grupo, 'LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES']
        self.frames = [tk.Frame(self) for i in range( len( calendarioExamenes ) )]
        # calendarioGrupo = [dias] + calendarioGrupo
        fechaInicio = self.addFechas(fechaInicio)
        fechaFinal = date( int(self.fechaFinal[0]), int(self.fechaFinal[1]), int(self.fechaFinal[2]))
        self.lbl = tk.Label(self.frameTitleAndButtons, text=self.parciales[self.index])
        self.lbl.grid(row=0, column=0,sticky="w", padx=(20, 0), pady=(20, 5))
        lastExamen = ''
        for currentCalendar in range( len(calendarioExamenes)):
            # fechaInicio += datetime.timedelta(days=2*currentCalendar)
            for column in range( len(self.buttons[currentCalendar][0]) ):
                diaEnCurso = calendarioExamenes[currentCalendar][0][column]
                bg='#FFFFFF'
                fg='#1E1E1E'
                state = 'disabled'
                color = '#FFFFFF'
                lastExamen = ''
                for row in range (len(self.buttons[currentCalendar])):
                    if column > 0:
                        if diaEnCurso > fechaFinal:
                            break
                    try:
                        materia = calendarioGrupo[row][column]['materia']
                    except:
                        materia = calendarioGrupo[row][column]
                    if row > 0:
                        try:
                            examen = calendarioExamenes[currentCalendar][row][column]['materia']
                        except:
                            examen = calendarioExamenes[currentCalendar][row][column]
                        if self.validarSiMateriaEsIgulAExamen(examen):
                            examen = ''
                    else:
                        examen = ''
                    if row == 0:
                        if column > 0:
                            if diaEnCurso > fechaFinal-datetime.timedelta(days=1):
                                break
                            materia = dias[column] + ' ' + datetime.datetime.strftime( calendarioExamenes[currentCalendar][0][column] , "%d/%m/%Y")
                            diaEnCurso = calendarioExamenes[currentCalendar][0][column]
                        else:
                            materia = dias[column]
                
                    # fechaInicio += datetime.timedelta(days=1)
                    elif row > 0  and column > 0:
                        if examen == 'inhabil':
                            bg='#2F2E35'
                            fg='#797689'
                            state = 'disabled'
                            materia = 'Día inhábil'
                        else:
                            if materia == examen :
                                lastExamen = materia
                                color = calendarioGrupo[row][column]['color']
                                bg= color
                                fg='#FFFFFF'
                                state='normal'
                            elif materia == lastExamen:
                                color = calendarioGrupo[row][column]['color']
                                bg= color
                                fg='#FFFFFF'
                                state='normal'
                                lastExamen = ''
                            else:
                                bg='#FFFFFF'
                                fg='#1E1E1E'
                                state = 'disabled'
                    
                    self.buttons[currentCalendar][row][column] = tk.Button(
                        self.frames[currentCalendar],
                        command= lambda m=materia,c=color, row=row, column=column, z=currentCalendar: self.disableAllcells(m,c,row,column,z),
                        text=materia, 
                        background=bg, 
                        foreground= fg,
                        state = state,
                        relief = 'flat')
                    self.buttons[currentCalendar][row][column].grid(row=row, column=column,sticky="nsew")
                    materia = ''

        for i in range( len(self.frames) ):
            self.frames[i].grid(row=i+1, column=0, columnspan=4, padx=20, pady=20,sticky="nsew")
            self.rowconfigure(i+1, weight=3)

    def printCalendarioExtraordinario(self, calendarioExamenes, grupo, calendarioGrupo, fechaInicio):
        self.buttons = [ [['' for x in range( len(self.calendarioGrupo[0])  ) ] for j in range( len(self.calendarioGrupo) )] for i in range( len(self.calendarioExamenes) )  ]
        dias = [grupo, 'LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES']
        self.frames = [tk.Frame(self) for i in range( len( calendarioExamenes ) )]
        
        fechaInicio = self.addFechas(fechaInicio)   
        fechaFinal = date( int(self.fechaFinal[0]), int(self.fechaFinal[1]), int(self.fechaFinal[2]))
        self.lbl = tk.Label(self.frameTitleAndButtons, text=self.parciales[self.index])
        self.lbl.grid(row=0, column=0,sticky="w", padx=(20, 0), pady=(20, 5))
        
        for currentCalendar in range( len(calendarioExamenes)):
            fechaInicio += datetime.timedelta(days=2*currentCalendar)
            for column in range( len(self.buttons[currentCalendar][0]) ):
                diaEnCurso = calendarioExamenes[currentCalendar][0][column]
                bg='#FFFFFF'
                fg='#1E1E1E'
                state = 'disabled'
                color = '#FFFFFF'
                for row in range (len(self.buttons[currentCalendar])):
                    if column > 0:
                        if diaEnCurso > fechaFinal:
                            break
                    try:
                        materia = calendarioGrupo[row][column]['materia']
                    except:
                        materia = calendarioGrupo[row][column]
                    try:
                        examen = calendarioExamenes[currentCalendar][row][column]['materia']
                    except:
                        examen = ''
                    if row == 0:
                        if column > 0:
                            if diaEnCurso > fechaFinal-datetime.timedelta(days=1):
                                break
                            materia = materia.upper() + ' ' + datetime.datetime.strftime( calendarioExamenes[currentCalendar][0][column] , "%d/%m/%Y")
                            diaEnCurso = calendarioExamenes[currentCalendar][0][column]
                        else:
                            materia = dias[column]
                    if row > 0 and column > 0:
                        if examen == 'inhabil':
                            bg='#2F2E35'
                            fg='#797689'
                            state = 'disabled'
                            materia = 'Día inhábil'
                            calendarioExamenes[currentCalendar][row][column] = ''

                        else:
                            if  examen != '':
                                color = "#FD5028"
                                bg= color
                                fg='#FFFFFF'
                                state='normal'
                                materia = examen
                            else:
                                bg='#FFFFFF'
                                fg='#1E1E1E'
                                state = 'disabled'
                    
                    self.buttons[currentCalendar][row][column] = tk.Button(
                        self.frames[currentCalendar],
                        command= lambda m=materia,c=color, row=row, column=column, z=currentCalendar: self.disableAllcells(m,c,row,column,z),
                        text=materia, 
                        state= state, 
                        background=bg, 
                        foreground= fg,
                        relief = 'flat')
                    self.buttons[currentCalendar][row][column].grid(row=row, column=column,sticky="nsew")
                    materia = ''

        for i in range( len(self.frames) ):
            self.frames[i].grid(row=i+1, column=0, columnspan=4, padx=20, pady=20,sticky="nsew")
            self.rowconfigure(i+1, weight=3)
            
    def printCalendarioPendiente(self, grupo,calendarioGrupo):
        self.buttons = [['' for x in range( len(self.calendarioGrupo[0])  ) ] for j in range( len(self.calendarioGrupo)+1 ) ]
        self.frames = [tk.Frame(self)]
        dias = [grupo, 'LUNES FECHA PENDIENTE', 'MARTES FECHA PENDIENTE', 'MIERCOLES FECHA PENDIENTE', 'JUEVES FECHA PENDIENTE', 'VIERNES FECHA PENDIENTE']

        calendarioGrupo = [dias] + calendarioGrupo
        self.lbl = tk.Label(self.frameTitleAndButtons, text=self.parciales[self.index])
        self.lbl.grid(row=0, column=0,sticky="w", padx=(20, 5), pady=(20, 5))
        
        for column in range( len(self.buttons[0]) ):
            bg='#FFFFFF'
            fg='#1E1E1E'
            state = 'disabled'
            for row in range (len(self.buttons)):
                try:
                    materia = calendarioGrupo[row][column]['materia']
                except:
                    materia = calendarioGrupo[row][column]
                
                self.buttons[row][column] = tk.Button(
                    self.frames[0],
                    text=materia, 
                    state= state, 
                    background=bg, 
                    foreground= fg,
                    relief = 'flat')
                self.buttons[row][column].grid(row=row, column=column,sticky="nsew")
        self.frames[0].grid(row=1, column=0, columnspan=4, padx=30, pady=20,sticky="nsew")
        self.rowconfigure(1, weight=3)

    def disableMateriaNoAplicada(self, index):
        self.btns[index].config(
            state= 'disabled', 
            background='#FFFFFF',
            foreground='#1E1E1E'
            )
        self.modificacionActivada = True

        for c in range( len(self.buttons) ):
            for row in range( len(self.buttons[c] ) ):
                for column in range( len(self.buttons[c][row]) ):
                    try:
                        bg = self.buttons[c][row][column]['background']
                    except:
                        continue
                    if bg == '#FFFFFF' and row >0:
                        materia = self.buttons[c][row][column]['text']
                        
                        self.buttons[c][row][column].config(
                            state= 'normal',
                            command= lambda m=materia,color='#31D68B',row=row,column=column,z=c: self.actifAllCells(m,color,z, row,column, True, index)
                        )
                    else:
                        self.buttons[c][row][column].config(
                            state= 'disable'
                        )
        
    def dosModulos(self, row, column, calendario):
        try:
            materia = calendario[row][column]['Materia']
            comparacion = calendario[row-1][column]['Materia']
            if materia == comparacion:
                return True
        finally:
            return False
    
    def disableAllcells(self, materia, color, row1, column1,z1, permissions=None, index=None, lastMateria=None):
        if self.modificacionActivada == False:
            self.celdaActivada = []
            self.celdaActivada.append({
                'row':row1,
                'column':column1,
                'z':z1
            })
            for z in range( len(self.buttons) ):
                for row in range( len(self.buttons[z] ) ):
                    for column in range( len(self.buttons[z][row] ) ):
                        if permissions != None:
                            self.calendarioGrupo[row1][column1]['materia'] = lastMateria
                            self.calendarioGrupo[row1][column1].pop('fecha', None)
                            self.buttons[z1][row1][column1]['text'] = lastMateria

                            self.buttons[z1][row1][column1].config(
                                    state= 'disabled', 
                                    background='#FFFFFF',
                                    foreground='#1E1E1E',
                                    command= lambda m = materia,c=color,z=z, i=row, j=column: self.actifAllCells(m,c,z,i,j)
                                    )
                            try:
                                color = self.buttons[z][row][column]['background']
                            except:
                                continue
                            if color == '#FFFFFF':
                                self.buttons[z][row][column].config(
                                    state= 'normal', 
                                    command= lambda m=materia,color='#FD6331',row=row,column=column,z=z1: self.actifAllCells(m,color,z, row,column, True, index)
                                    )
                            else:
                                self.buttons[z][row][column].config(
                                    state= 'disabled', 
                                    command= lambda m = materia,c=color,z=z, i=row, j=column: self.actifAllCells(m,c,z,i,j)
                                    )
                            if row == 0:
                                self.buttons[z][row][column].config(
                                    state= 'disabled', 
                                    command= lambda m = materia,c=color,z=z, i=row, j=column: self.actifAllCells(m,c,z,i,j)
                                    )
                        else:
                            if self.index < 4:
                                try:
                                    comparacion = self.buttons[z][row][column]['text']
                                except:
                                    continue
                                if  comparacion == materia:
                                    self.buttons[z][row][column].config(
                                        state= 'normal', 
                                        background='#FFFFFF',
                                        foreground='#1E1E1E',
                                        command= lambda m = materia,c=color,z=z, i=row, j=column: self.actifAllCells(m,c,z,i,j)
                                        )
                                    try:
                                        siguiente = self.buttons[z][row+1][column]['text']
                                        if siguiente == materia:
                                            self.buttons[z][row+1][column].config(
                                            state= 'normal', 
                                            background='#FFFFFF',
                                            foreground='#1E1E1E',
                                            text=materia,
                                            command= lambda m = materia,c=color,z=z, i=row, j=column: self.actifAllCells(m,c,z,i,j)
                                            )
                                    except:
                                        pass
                                    try:
                                        anterior = self.buttons[z][row-1][column]['text']
                                        if anterior == materia:
                                            self.buttons[z][row-1][column].config(
                                            state= 'normal', 
                                            background='#FFFFFF',
                                            foreground='#1E1E1E',
                                            text=materia,
                                            command= lambda m = materia,c=color,z=z, i=row, j=column: self.actifAllCells(m,c,z,i,j)
                                            )
                                    except:
                                        pass
                                    
                                else:
                                    self.buttons[z][row][column].config(state= 'disabled')
                            #Examenes extraOrdinarios
                            else:
                                self.buttons[z1][row1][column1].config(
                                        state= 'normal', 
                                        background='#FFFFFF',
                                        foreground='#1E1E1E',
                                        command= lambda m = materia,c=color,z=z, i=row, j=column: self.actifAllCells(m,c,z,i,j)
                                        )
                                try:
                                    color = self.buttons[z][row][column]['background']
                                except:
                                    continue
                                if color == '#FFFFFF':
                                    self.buttons[z][row][column].config(
                                        state= 'normal', 
                                        command= lambda m = materia,c=color,z=z, i=row, j=column: self.actifAllCells(m,c,z,i,j)
                                        )
                                else:
                                    self.buttons[z][row][column].config(
                                        state= 'disabled', 
                                        command= lambda m = materia,c=color,z=z, i=row, j=column: self.actifAllCells(m,c,z,i,j)
                                        )
                                if row == 0:
                                    self.buttons[z][row][column].config(
                                        state= 'disabled', 
                                        command= lambda m = materia,c=color,z=z, i=row, j=column: self.actifAllCells(m,c,z,i,j)
                                        )

            self.modificacionActivada = True

    #Este metodo activa las celdas despues de haber seleccionado una nueva materia
    def actifAllCells(self, materia, color,z,i,j, permissions=None, index=None):
        
        if i != 0:
            if permissions != True:
                #Elimina la informacion del arreglo de examenes 
                z1 = int(self.celdaActivada[0]['z'])
                row1 = int(self.celdaActivada[0]['row']) 
                column1 = int(self.celdaActivada[0]['column'])

                info = self.listCalendarios[self.index][z1][row1][column1]
                if self.index < 4:
                    if info == '':
                        info = self.listCalendarios[self.index][z1][row1-1][column1]
                        self.listCalendarios[self.index][z1][row1-1][column1] = ''
                    else:
                        self.listCalendarios[self.index][z1][row1][column1] = ''
                else:
                    color = '#FD5028'
                    self.listCalendarios[self.index][z1][row1][column1] = ''
            else:
                info = self.calendarioGrupo[i][j]
                try:
                    newMateria = self.listaMateriasNoAplicadas[self.index][index]
                    self.listaMateriasNoAplicadas[self.index].pop(index)
                except:
                    newMateria = materia
                lastMateria = self.calendarioGrupo[i][j]['materia']
                info['materia'] = newMateria
                try:
                    z1 = int(self.celdaActivada[0]['z'])
                    row1 = int(self.celdaActivada[0]['row']) 
                    column1 = int(self.celdaActivada[0]['column'])
                    self.listCalendarios[self.index][z1][row1][column1] = ''
                except:
                    pass


            nuevafecha = self.buttons[z][0][j]['text'].split(' ')
            nuevafecha= nuevafecha[1].split('/')
            dia = int(nuevafecha[0])
            mes = int(nuevafecha[1])
            anio = int(nuevafecha[2])
            nuevafecha = date(anio, mes, dia)
            try:
                info['fecha'] = nuevafecha
            except:
                pass

            if self.index < 4:
                # a = self.calendarioGrupo[z][i][j]
                # b = self.calendarioGrupo[z][i-1][j]
                a = self.calendarioGrupo[i][j]
                b = self.calendarioGrupo[i-1][j]
                if  a == b and a != '' and b != '':
                    self.listCalendarios[self.index][z][i-1][j] = info
                else:
                    self.listCalendarios[self.index][z][i][j] = info
            else:
                self.listCalendarios[self.index][z][i][j] = info

            if self.modificacionActivada:
                if permissions != None:
                    color = '#31D68B'
                    self.buttons[z][i][j].config(
                        state= 'normal', 
                        background=color,
                        foreground='#FFFFFF',
                        text=newMateria,
                        command= lambda m=newMateria,c=color,row=i,column=j,z=z, permissions = True, index=index, lastMateria= lastMateria: 
                        self.disableAllcells(m,c,row,column,z, permissions, index, lastMateria)
                    )
                else:
                    self.buttons[z][i][j].config(
                        state= 'normal', 
                        background=color,
                        foreground='#FFFFFF',
                        text=materia,
                        command= lambda m=materia,c=color,row=i,column=j,z=z: self.disableAllcells(m,c,row,column,z)
                    )
                    if self.index < 4:
                        try:
                            siguiente = self.buttons[z][i+1][j]['text']
                            if siguiente == materia:
                                self.buttons[z][i+1][j].config(
                                state= 'normal', 
                                background=color,
                                foreground='#FFFFFF',
                                command= lambda m=materia,c=color,row=i,column=j,z=z: self.disableAllcells(m,c,row,column,z)
                                )
                        except:
                            pass
                        try:
                            anterior = self.buttons[z][i-1][j]['text']
                            if anterior == materia:
                                self.buttons[z][i-1][j].config(
                                state= 'normal', 
                                background=color,
                                foreground='#FFFFFF',
                                command= lambda m=materia,c=color,row=i,column=j,z=z: self.disableAllcells(m,c,row,column,z)
                                )
                                # self.listCalendarios[self.index][z][i][j] = ''
                                # self.listCalendarios[self.index][z][i-1][j] = info
                        except:
                            pass

                        for c in range( len(self.buttons) ):
                            for row in range( len(self.buttons[c] ) ):
                                for column in range( len(self.buttons[c][row]) ):
                                    try:
                                        bg = self.buttons[c][row][column]['background']
                                    except:
                                        continue
                                    if bg == '#FFFFFF' or bg == '#2F2E35':
                                        self.buttons[c][row][column].config(state= 'disabled')
                                    else:
                                        self.buttons[c][row][column].config(state= 'normal')
            #Examenes extraordinarios
            else:
                for c in range( len(self.buttons) ):
                    for row in range( len(self.buttons[c] ) ):
                        for column in range( len(self.buttons[c][row]) ):
                            try:
                                bg = self.buttons[c][row][column]['background']
                            except:
                                continue
                            if bg == '#FFFFFF' or bg == '#2F2E35':
                                self.buttons[c][row][column].config(state= 'disabled')
                            else:
                                materia = self.buttons[c][row][column]['text']
                                self.buttons[c][row][column].config(
                                    state= 'normal',
                                    command= lambda m=materia,c=color,row=row,column=column,z=c: self.disableAllcells(m,c,row,column,z)
                                )
            if permissions != None:
                for c in range( len(self.buttons) ):
                    for row in range( len(self.buttons[c] ) ):
                        for column in range( len(self.buttons[c][row]) ):
                            try:
                                bg = self.buttons[c][row][column]['background']
                            except:
                                continue
                            if bg == '#FFFFFF' or bg == '#2F2E35':
                                self.buttons[c][row][column].config(state= 'disabled')
                            else:
                                materia = self.buttons[c][row][column]['text']
                                self.buttons[c][row][column].config(
                                    state= 'normal'
                                )

            self.modificacionActivada = False

        
            
    def addFechas(self, fechaInicio):
        f = (fechaInicio).weekday()
        while f > 0:
            fechaInicio -= datetime.timedelta(days=1)
            f -= 1 
        return fechaInicio

    def nextCalendario(self, argv):
        if self.validarSiSeAsignaronMateriasNoAplicadas():
            if self.index < 5:
                self.clear()
                self.index+=1
                self.calendarioExamenes = self.listCalendarios[self.index] 
                self.grupo = argv[0][3]
                self.calendarioGrupo = [self.dias] + argv[0][1]
                self.fechaInicio = argv[0][2][self.index]
                self.fechaFinal = argv[0][4][self.index]

                if self.calendarioExamenes != 'Pendiente':
                    if self.index < 4:
                        self.printCalendario(self.calendarioExamenes, self.grupo, self.calendarioGrupo, self.fechaInicio)
                    else:
                        self.printCalendarioExtraordinario(self.calendarioExamenes, self.grupo, self.calendarioGrupo, self.fechaInicio)
                else:
                    self.printCalendarioPendiente(self.grupo, self.calendarioGrupo)
            if self.index >= 5:
                self.btn2.config(
                    text="Crear Excel",
                    command= lambda : self.createExcel()
                )
            if self.index > 0:
                self.btn1.config(
                    state="normal"
                )
            self.printListaMateriasNoAplicadas()
        else:
            tk.messagebox.showwarning(parent=self, message="Recuerde asignar todas las materias Pendientes", title="Asignación de materias")
  
    
    def lastCalendario(self, argv):
        if self.validarSiSeAsignaronMateriasNoAplicadas():
            if self.index > 0:
                self.clear()
                self.index-=1
                self.calendarioExamenes = self.listCalendarios[self.index] 
                self.grupo = argv[0][3]
                self.calendarioGrupo = [self.dias] + argv[0][1]
                self.fechaInicio = argv[0][2][self.index]
                self.fechaFinal = argv[0][4][self.index]
                
                if self.calendarioExamenes != 'Pendiente':
                    if self.index < 4:
                        self.printCalendario(self.calendarioExamenes, self.grupo, self.calendarioGrupo, self.fechaInicio)
                    else:
                        self.printCalendarioExtraordinario(self.calendarioExamenes, self.grupo, self.calendarioGrupo, self.fechaInicio)
                else:
                    self.printCalendarioPendiente(self.grupo, self.calendarioGrupo)
            if self.index == 0:
                self.btn1.config(
                    state="disabled"
                )
            if self.index < 5:
                self.btn2.config(
                    text="Siguiente",
                    command= lambda : self.nextCalendario(argv)
                )
            self.printListaMateriasNoAplicadas()
        else:
            tk.messagebox.showwarning(parent=self, message="Recuerde asignar todas las materias Pendientes", title="Asignación de materias")
    
    def clear(self):
        # list = self.grid_slaves()
        # for l in list:
        #     l.destroy()
        self.lbl.destroy() 
        for f in self.frames:
            f.destroy()
    
    def addHorarios(self, array, array2):
        for row in range( len(array) ):
            array2[row][0] = array[row][0]
        return array2

    def createExcel(self):
        try:
            excel = excelCreator(self.listCalendarios, self.grupo, self.fechas, self.calendarioGrupo)
            excel.createExcel()
            tk.messagebox.showinfo(parent=self, message="Se ha generado con exito el Excel", title="Generar Excel")
            os.system('start excel.exe "%s\\calendario.xlsx"' % (sys.path[0], ))
        except:
            tk.messagebox.showwarning(parent=self, message="No se ha podido completar la acción", title="Generar Excel")

    def validarSiSeAsignaronMateriasNoAplicadas(self):
        try:
            if len(self.listaMateriasNoAplicadas[self.index]) > 0:
                return False
            else:
                return True
        except:
            return True
    
    def validarSiMateriaEsIgulAExamen(self, materia):
        try:
            if len(self.listaMateriasNoAplicadas2[self.index]) > 0:
                for item in self.listaMateriasNoAplicadas2[self.index]:
                    if item == materia:
                        return True
                return False
            return False
        except:
            return False


