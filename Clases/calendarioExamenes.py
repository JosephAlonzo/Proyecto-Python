#   *************************************                                 
#   **                                 **
#   **       autor: Alonzo joseph      **
#   **        fecha: 17/10/2019        **
#   **               UTM               **
#   **                                 **
#   *************************************

from Clases.calendario import Calendario
import datetime
from datetime import date,timedelta
import operator

class CalendarioExamenes():
    def __init__(self,array,grupo,diasInhabiles, fechaFinal):
        #Calendario.__init__(self)
        self.diasInhabiles = diasInhabiles
        self.dias = [grupo, 'Lunes','Martes','Miercoles','Jueves','Viernes']
        self.calendarioUtm = [self.dias] + array
        self.periodo = []
        self.fechaFinal = fechaFinal
        self.fechaInicio = ''
        
        self.materiasSinExamenes = ['tutorias', 'ingles','tutorías', 'inglés'   ]
        self.listaMateriasNoAplicadas = []
    def crearCalendarioExmanes(self):
        #esta parte crea los arreglos de los calendarios que vamos a utilizar
        numeroSemanas = self.calcularNumeroDeSemanasEnIntervalo(self.fechaFinal, 5)
        self.calendarioUtmExamenes = [ 
           [ [ '' for x in range( len(self.dias))] for y in range(len(self.calendarioUtm)) ] for i in range(numeroSemanas+1)
        ]
        self.calendarioUtm = self.deleteMateriasDondeNoSePresentaExamen(self.calendarioUtm, self.materiasSinExamenes)
        self.addFechas()
        # 'diaDeInicio' es el valor numerico del dia de inicio, se le agrega uno porque es base cero 
        # y en nuestro arreglo de calendarios el valor '0' es ocupado por los horarios
        diaDeInicio = self.fechaInicio.weekday() + 1
        listaMaterias = self.getLisOrderedByPriority(self.calendarioUtm, numeroSemanas, diaDeInicio)

        i = len(self.calendarioUtm)
        j = len(self.calendarioUtm[0])
        limiteExamenesPorDia = 2
        # diaEnCurso = self.fechaInicio 
        ultimaMateria = ''
        count = 0
        while len(listaMaterias) > 0:
            #Despues de pasar los calendarios si aun es la misma materia listaMaterias[0][0] 
            # con respecto a ultimaMateria entonces esto quiere decir que no se encontro la clase de 2 modulos lo que 
            # por eso en cantidad en el arreglo disminuye a cero lo que quiere decir que podra agregarse a un solo modulo
            # si es necesario
            if ultimaMateria == listaMaterias[0][0]:
                if listaMaterias[0][1] == 0 and count == 3:
                    self.listaMateriasNoAplicadas.append(
                        listaMaterias[0][0]
                    )
                    
                    listaMaterias.pop(0)
                    count = 0
                elif count > 0:
                    newLista = []
                    for x in range(len(listaMaterias)):
                        if x == 0:
                            newLista.append((listaMaterias[x][0], 0))
                        else:
                            newLista.append((listaMaterias[x][0], listaMaterias[x][1]))
                    listaMaterias = newLista
                    count += 1
                else:
                    count = 1

            if len(listaMaterias) > 0:
                ultimaMateria = listaMaterias[0][0]
            for semana in range(len(self.calendarioUtmExamenes)):
                # diaEnCurso += datetime.timedelta(days=2 * semana)
                # if diaEnCurso > self.fechaFinal:
                #     diaEnCurso = self.fechaInicio
                for column in range(j):
                    # if column == 0 or (column < diaDeInicio and semana == 0):
                    if column == 0:
                        continue
                    diaEnCurso = self.calendarioUtmExamenes[semana][0][column]
                    if diaEnCurso < self.fechaInicio:
                        continue
                    if diaEnCurso > self.fechaFinal:
                        break

                    if self.validarExamenesAsignadosPorDia(self.calendarioUtmExamenes[semana], column, limiteExamenesPorDia):
                        # diaEnCurso += datetime.timedelta(days=1)
                        continue
                    if self.isInhabil(diaEnCurso) == True:
                        for row in range(i):
                            if row == 0:
                                continue
                            self.calendarioUtmExamenes[semana][row][column] = 'inhabil'
                        # diaEnCurso += datetime.timedelta(days=1)
                        continue
                    for row in range(i):
                        if row == 0:
                            continue
                        try:
                            materia = self.calendarioUtm[row][column]['materia']
                        except:
                            materia = self.calendarioUtm[row][column]
                        try:
                            comparacion = listaMaterias[0][0]
                        except:
                            break
                        if materia == comparacion:
                            if self.validarSiMateriaEsDeDosModulos(self.calendarioUtm,column, row, materia):
                                self.calendarioUtmExamenes[semana][row][column] = self.calendarioUtm[row][column]
                                self.calendarioUtmExamenes[semana][row][column].update( {'fecha': diaEnCurso} )
                                listaMaterias.pop(0)
                                count = 0
                                break
                            else:
                                if listaMaterias[0][1] == 0:
                                    self.calendarioUtmExamenes[semana][row][column] = self.calendarioUtm[row][column]
                                    self.calendarioUtmExamenes[semana][row][column].update( {'fecha': diaEnCurso} )
                                    listaMaterias.pop(0)
                                    count = 0
                                    break
                                continue
                    # diaEnCurso += datetime.timedelta(days=1)
                    
                    # f = (diaEnCurso).weekday()
                    # if  f > 4:
                    #     break
                    # if diaEnCurso > self.fechaFinal:
                    #     break
                
                
        return self.calendarioUtmExamenes

    def crearCalendarioExamenesExtraordinarios(self):
        self.materiasSinExamenes = ['ingles', 'inglés']
        fechaFinal = self.fechaFinal
        numeroSemanas = self.calcularNumeroDeSemanasEnIntervalo(self.fechaFinal, 1)
        self.calendarioUtmExamenes = [ 
           [ [ '' for x in range( len(self.dias))] for y in range(len(self.calendarioUtm)) ] for i in range(numeroSemanas+1)
        ]
        self.calendarioUtm = self.deleteMateriasDondeNoSePresentaExamen(self.calendarioUtm, self.materiasSinExamenes)
        self.addFechas()
        # 'diaDeInicio' es el valor numerico del dia de inicio, se le agrega uno porque es base cero 
        # y en nuestro arreglo de calendarios el valor '0' es ocupado por los horarios
        diaDeInicio = self.fechaInicio.weekday() + 1
        listaMaterias = self.getLisOrderedByPriority(self.calendarioUtm, numeroSemanas,diaDeInicio)
        i = len(self.calendarioUtm)
        j = len(self.calendarioUtm[0])
        semana = 0
        dia = 1
        # diaEnCurso = self.fechaInicio 

        while len(listaMaterias) > 0:
            # diaDeInicio = self.fechaInicio.weekday() + 1
            for semana in range(len(self.calendarioUtmExamenes)):
                if len(listaMaterias) < 1:
                    break
                # diaEnCurso += datetime.timedelta(days=2 * semana)
                # if diaEnCurso > self.fechaFinal:
                #     diaEnCurso = self.fechaInicio
                for column in range(j):
                    if len(listaMaterias) < 1:
                        break
                    if column == 0:
                        continue
                    diaEnCurso = self.calendarioUtmExamenes[semana][0][column]
                    if diaEnCurso < self.fechaInicio:
                        continue
                    if self.isInhabil(diaEnCurso) == True:
                        for row in range(i):
                            if row == 0:
                                continue
                            self.calendarioUtmExamenes[semana][row][column] = 'inhabil'
                        continue
                    for row in range(i):
                        if row == 0:
                            continue
                        try:
                            materia = self.calendarioUtm[row][column]['materia']
                        except:
                            materia = self.calendarioUtm[row][column]
                        if len(listaMaterias) < 1:
                            break
                        if materia != '':
                            self.calendarioUtmExamenes[semana][row][column] = self.calendarioUtm[row][column]
                            self.calendarioUtmExamenes[semana][row][column].update( {'fecha': diaEnCurso} )
                            self.calendarioUtmExamenes[semana][row][column].update( {'materia': listaMaterias[0][0]} )
                            listaMaterias.pop(0)
                           
                    diaEnCurso += datetime.timedelta(days=1)
                    if diaEnCurso > self.fechaFinal:
                        break
            
                if diaEnCurso > self.fechaFinal:
                    dia+=1
                    tempCalendar = self.calendarioUtmExamenes[0]
                    numeroSemanas = self.calcularNumeroDeSemanasEnIntervalo(fechaFinal, dia)
                    self.calendarioUtmExamenes = [ 
                        [[ '' for x in range( len(self.dias))] for y in range(len(self.calendarioUtm)) ] for i in range(numeroSemanas+1)
                    ]
                    self.addFechas()
                    self.calendarioUtmExamenes[numeroSemanas] = tempCalendar
                    # diaEnCurso = self.fechaInicio
                    break

        self.addDiasInhabilesInInterface(i,j)       
        return self.calendarioUtmExamenes

    def addDiasInhabilesInInterface(self, i, j):
        for semana in range(len(self.calendarioUtmExamenes)):
            for column in range(j):
                if column == 0:
                    continue
                diaEnCurso = self.calendarioUtmExamenes[semana][0][column]
                if diaEnCurso < self.fechaInicio:
                    continue
                if self.isInhabil(diaEnCurso) == True:
                    for row in range(i):
                        if row == 0:
                            continue
                        self.calendarioUtmExamenes[semana][row][column] = 'inhabil'

    def getLisOrderedByPriority(self, array, numeroDeSemanas, diaDeInicio):
        listaMaterias = []
        listaMaterias2 = []

        for semana in range(numeroDeSemanas + 1):
            for column in range(len(array[0])):
                if column == 0:
                    continue
                if column < diaDeInicio and semana == 0 and numeroDeSemanas > 0:
                    continue
                for row in range(len(array)):
                    if row == 0:
                        continue
                    if array[row][column] != '':
                        materia = array[row][column]['materia']
                        if materia[0:6].lower() != 'inglés' and materia[0:8].lower() != 'tutorías' and materia != 'modulo libre' and materia[0:6].lower() != 'ingles' and materia[0:8].lower() != 'tutorias':
                            try:
                                if array[row+1][column] != '':
                                    nextMateria = array[row+1][column]['materia']
                                else:
                                    nextMateria = ''
                            except:
                                nextMateria = ''
                            if materia == nextMateria:
                                listaMaterias.append( materia )
                                if len(array) < row+1:
                                    row+=1
                            if listaMaterias2.count(materia) < 1:
                                listaMaterias2.append(materia)

        for item in range(len(listaMaterias2)):
            listaMaterias2[item] = ( listaMaterias2[item], listaMaterias.count(listaMaterias2[item]) )
             
        listaMaterias2.sort(key = operator.itemgetter(1))
        return listaMaterias2

    def validarExamenesAsignadosPorDia(self, calendario, column, numeroDeMateriasPorDia):
        count = 0
        for row in range( len(calendario) ):
            if row == 0:
                continue
            if calendario[row][column] != '':
                count += 1
                if count >= numeroDeMateriasPorDia:
                    return True
        return False
    
    def validarSiMateriaEsDeDosModulos(self, calendario, column, row, materia):
        largo = len(calendario)-1
        if row >= largo:
            return False
        try:
            comparacion = calendario[row+1][column]['materia']
        except:
            return False
        if materia == comparacion:
            return True
        return False
        
    def deleteMateriasDondeNoSePresentaExamen(self, calendario, materias):
        for materia in materias:
            for row in range(len(calendario)):
                if row == 0:
                    continue
                for column in range(len(calendario[row])):
                    if column == 0:
                        continue
    
                    materiaEnCalendario = calendario[row][column]
                    if materiaEnCalendario != '':
                        materiaEnCalendario = calendario[row][column]['materia'][0:len(materia)]
                        materiaEnCalendario = materiaEnCalendario.lower()
                        if materiaEnCalendario== materia.lower():
                            calendario[row][column] = ''
        return calendario

    def calcularNumeroDeSemanasEnIntervalo(self, fechaFinal, cantidadDias):
        dia = int(fechaFinal[2])
        mes = int(fechaFinal[1])
        anio = int(fechaFinal[0])
        fecha = date(anio, mes, dia)
        fechaFinal = fecha - datetime.timedelta(days=1)
        fechaInicio = fecha - datetime.timedelta(days=1)
        diasEntreSemana = 0
        i=0
        while diasEntreSemana < cantidadDias:
            dia = fechaFinal - datetime.timedelta(days=i)
            f = (dia).weekday()
            if  f < 5 and self.isInhabil(dia) != True:
                diasEntreSemana += 1
            if diasEntreSemana < cantidadDias:
                fechaInicio -= datetime.timedelta(days=1)
            i+=1
        
        #isocalendar devuelve [0] año, [1] numero de semana, [2] dia de la semana
        d1 = fechaFinal.isocalendar()[1]
        d2 = fechaInicio.isocalendar()[1] 
        result = d1 - d2 
        self.fechaFinal = fechaFinal
        self.fechaInicio = fechaInicio
        

        return result

    def addFechas(self):
        diaDeInicio = self.fechaInicio
        diaDeInicio = self.fechaInicio - datetime.timedelta(days=diaDeInicio.weekday() ) 
        for semana in range(len(self.calendarioUtmExamenes)):
            diaDeInicio += datetime.timedelta(days=2 * semana)
            for column in range(len(self.calendarioUtmExamenes[semana][0])):
                # if column == 0 or (column < diaDeInicio and semana == 0):
                #     continue
                if column == 0:
                    continue
                self.calendarioUtmExamenes[semana][0][column] = diaDeInicio
                diaDeInicio += datetime.timedelta(days=1)

    def isInhabil(self, dia):
        try:
            for diaInhabil in self.diasInhabiles:
                x = str(diaInhabil).split('-')
                comparacion = date( int(x[0]), int(x[1]), int(x[2]))
                if dia == comparacion:
                    return True
            return False
        except:
            return False


# obj = calendarioExamenes()
# obj.crearCalendarioExmanes()
# obj.printCalendarioExamenes()


    
    
