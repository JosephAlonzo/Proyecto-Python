#   *************************************                                 
#   **                                 **
#   **       autor: Alonzo joseph      **
#   **        fecha: 17/10/2019        **
#   **               UTM               **
#   **                                 **
#   *************************************

from Clases.calendario import Calendario
import unidecode
import datetime
from datetime import date,timedelta

class CalendarioExamenes():
    def __init__(self,array,grupo,diasInhabiles, fechaFinal):
        #Calendario.__init__(self)
        self.diasInhabiles = diasInhabiles
        self.dias = [grupo, 'Lunes','Martes','Miercoles','Jueves','Viernes']
        self.calendarioUtm = array
        self.periodo = []
        self.fechaFinal = fechaFinal
        self.fechaInicio = ''
        #esta parte crea los arreglos de los calendarios que vamos a utilizar
        self.numeroSemanas = self.calcularNumeroDeSemanasEnIntervalo(self.fechaFinal)
        self.calendarioUtmExamenes = [ 
           [ [ '' for x in range( len(self.dias))] for y in range(len(self.calendarioUtm)) ] for i in range(self.numeroSemanas+1)
        ]
        #self.materiasSinExamenes = materiasSinExamenes

    def crearCalendarioExmanes(self):
        # for i in range( len (self.calendarioUtmExamenes) ) :
        #     self.calendarioUtmExamenes[i] = self.addHorasAndDias(self.calendarioUtmExamenes[i])   
            
        # self.calendarioUtm = self.deleteMateriasDondeNoSePresentaExamen(self.calendarioUtm, self.materiasSinExamenes)
        i = len(self.calendarioUtm)
        j = len(self.calendarioUtm[0])
        salir = False
        limiteExamenesPorDia = 1
        semana = 0
        diaEnCurso = self.fechaInicio
        while salir == False:
            for column in range(j):
                # 'diaDeInicio' es el valor numerico del dia de inicio, se le agrega uno porque es base cero 
                # y en nuestro arreglo de calendarios el valor '0' es ocupado por los horarios
                diaDeInicio = self.fechaInicio.weekday() + 1
                if column == 0 or (column < diaDeInicio and semana == 0):
                    continue
                # diaEnCurso representa la fecha de inicio nos servira para validar si es 
                # un dia inhabil cuando la semana vuelve a ser 0 se reinicia esta variable
                # para indicar que volveremos a pasar por la misma semana
                diaEnCurso += datetime.timedelta(days=1)
                if self.isInhabil(diaEnCurso) == True:
                    continue
                for row in range(i):
                    # if row == 0:
                    #     continue
                    try:
                        materia = self.calendarioUtm[row][column]['materia']
                    except:
                        materia = self.calendarioUtm[row][column]

                    if  materia != '' and materia != 'modulo libre':
                        if self.validarExamenesAsignadosPorDia(self.calendarioUtmExamenes[semana], column, limiteExamenesPorDia):
                            break
                        self.calendarioUtmExamenes[semana][row][column] = self.calendarioUtm[row][column]
                        self.calendarioUtmExamenes[semana][row][column].update( {'fecha': diaEnCurso, 'dia': self.dias[diaEnCurso.weekday()]} )
                        self.calendarioUtm = self.deleteMateriasRepetidas(self.calendarioUtm, self.calendarioUtm[row][column]['materia'])
                        break
                        
                
            # Indico que sera el siguiente arreglo (o sea la siguiente semana)
            # como no hay sabados ni domingos al 'diaEnCurso' le agrego 2 dias que 
            # vendrian siendo el fin de semana esto con el fin de poder validar los dias inhabiles 
            semana += 1
            diaEnCurso += datetime.timedelta(days=2)
            if semana > self.numeroSemanas:
                # inidica que llegamos al fin de las semanas y si aun quedan materias vamos a volver a recorrer los arreglos para 
                # terminar de llenarlos
                semana = 0
                diaEnCurso = self.fechaInicio
                limiteExamenesPorDia += 1

            salir = self.validarSiTodosLosExamenesFueronAplicados()
        return self.calendarioUtmExamenes

    #Elimina las materias en las cuales ya fueron asignadas como examenes       
    def deleteMateriasRepetidas(self, calendario, materia):
        for i in range(len(calendario)):
            for j in range(len(calendario[i])):
                if j == 0:
                    continue
                try:
                    materiaEnCalendario = self.calendarioUtm[i][j]['materia']
                except:
                    materiaEnCalendario = self.calendarioUtm[i][j]
                    
                if materiaEnCalendario != '':
                    if materiaEnCalendario == materia:
                        calendario[i][j] = ''
        return calendario
    
    def validarExamenesAsignadosPorDia(self, calendario, column, numeroDeMateriasPorDia):
        count = 0
        for row in range( len(calendario) ):
            if calendario[row][column] != '':
                count += 1
                if count >= numeroDeMateriasPorDia:
                    return True
        return False

    def deleteMateriasDondeNoSePresentaExamen(self, calendario, materias):
        for materia in materias:
            for i in range(len(calendario)):
                if i == 0:
                    continue
                for j in range(len(calendario[i])):
                    if j == 0:
                        continue
                    materiaEnCalendario = calendario[i][j]
                    if materiaEnCalendario != '':
                        materiaEnCalendario[0] = unidecode.unidecode(materiaEnCalendario[0]).lower()
                        if materiaEnCalendario[0]== materia.lower():
                            calendario[i][j] = ''
        return calendario

    def validarSiTodosLosExamenesFueronAplicados(self):
        for i in range(len(self.calendarioUtm)):
            # if i == 0:
            #     continue
            for j in range(len(self.calendarioUtm[i])):
                if j == 0:
                    continue
                try:
                    materiaEnCalendario = self.calendarioUtm[i][j]['materia']
                    if materiaEnCalendario == 'modulo libre':
                        continue
                except:
                    materiaEnCalendario = self.calendarioUtm[i][j]

                if materiaEnCalendario != '':
                    return False
        return True

    def printCalendarioExamenes(self):
        i = len(self.calendarioUtmExamenes[0])
        j = len(self.calendarioUtmExamenes[0][0])
        diaEnCurso = self.fechaInicio
        encabezadoDia = ""
        for semana in range(len(self.calendarioUtmExamenes)):
            print("\n ************* Semana " + str(semana+1) + " ****************")
            for column in range(j):
                EmpezarDia = self.fechaInicio.weekday()+1
                if column == 0 or (column < EmpezarDia and semana == 0):
                    continue
                diaEnCurso += datetime.timedelta(days=1)
                for row in range(i):
                    if self.calendarioUtmExamenes[semana][row][column] != '':
                        if self.isInhabil(diaEnCurso) == True:
                            dia = self.calendarioUtmExamenes[semana][row][column]
                            dia = self.completarNombreImpresion(dia)
                            print( "El "+ dia +" " + str(diaEnCurso) +" es día inhabil \n")
                        else:
                            if row == 0:
                                dia = self.calendarioUtmExamenes[semana][row][column]
                                dia = self.completarNombreImpresion(dia)
                                encabezadoDia =  dia + " " + str(diaEnCurso) + "\n" 
                            else:
                                if encabezadoDia != "":
                                    print (encabezadoDia)
                                    encabezadoDia = ""
                                texto = ""
                                for item in self.calendarioUtmExamenes[semana][row][column]:
                                    texto += item + "\n"
                                print(texto)

    def calcularNumeroDeSemanasEnIntervalo(self, fechaFinal):
        dia = int(fechaFinal[2])
        mes = int(fechaFinal[1])
        anio = int(fechaFinal[0])
        fecha = date(anio, mes, dia)
        fechaFinal = fecha - datetime.timedelta(days=1)
        fechaInicio = fecha - datetime.timedelta(days=1)
        diasEntreSemana = 0
        i=0
        while diasEntreSemana < 5:
            dia = fechaFinal - datetime.timedelta(days=i)
            f = (dia).weekday()
            if  f < 5 and self.isInhabil(dia) != True:
                diasEntreSemana += 1
            if diasEntreSemana < 5:
                fechaInicio -= datetime.timedelta(days=1)
            i+=1
        
        #isocalendar devuelve [0] año, [1] numero de semana, [2] dia de la semana
        d1 = fechaFinal.isocalendar()[1]
        d2 = fechaInicio.isocalendar()[1] 
        result = d1 - d2 
        self.fechaInicio = fechaInicio
        return result

    def isInhabil(self, dia):
        for diaInhabil in self.diasInhabiles:
            x = str(diaInhabil).split('-')
            comparacion = date( int(x[0]), int(x[1]), int(x[2]))
            if dia == comparacion:
                return True
        return False

    def completarNombreImpresion(self, dia):
        if dia.lower() == "lu":
            return "Lunes"
        elif dia.lower() == "ma":
            return "Martes"
        elif dia.lower() == "mi":
            return "Miercoles"
        elif dia.lower() == "ju":
            return "Jueves"
        else:
            return "Viernes"

# obj = calendarioExamenes()
# obj.crearCalendarioExmanes()
# obj.printCalendarioExamenes()


    
    
