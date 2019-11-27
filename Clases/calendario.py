#   *************************************                                 
#   **                                 **
#   **       autor: Alonzo joseph      **
#   **        fecha: 12/10/2019        **
#   **               UTM               **
#   **                                 **
#   *************************************

from xml.dom import minidom

class Calendario():
    def __init__(self):
        self.onlyText = []
        self.salones = []
        self.clases = []
        self.horarios = []
        self.dias = []
        self.calendario = []
        self.sumas = []
        # Es la medida en unidades del cuadro de los horarios en el calendario
        # 2.0: Aqui se puede desmadrar checar despues 13/10/2019 
        self.referencia_de_x = 250

    def crearCalendario(self, svg):
        self.doc = minidom.parseString(svg)
        self.texts = [self.doc.getElementsByTagName('text')]
        self.rect = [self.doc.getElementsByTagName('rect')]
        
        i = 0
        j = 0
        for item in self.texts[0]:
            try:
                # En esta parte divido si sera un de la barra lateral izquierda o sera de las materias
                self.setHoras(item)
                if i < 6:
                    self.setDias(item)
                else:
                    if item.childNodes[0].data[0:3].upper() == "LAB" or item.childNodes[0].data[0:4].upper() == "AULA":
                        self.salones.append(
                            item.childNodes[0].data
                        )
            except:
                continue
            i += 1
        # Recupera la informacion de los cuadros de la imagen
        for item in self.rect[0]:
            try:
                informacion = item.childNodes[0].childNodes[0].data.split("\n")
                color = item._attrs['style'].firstChild.data[5:]
                atributos = {'x': item._attrs['x'].value, 'y': item._attrs['y'].value,
                             'height': item._attrs['height'].value}
                # Eliminamos la ultima porque los salones estan mal :O en el nodo RECT pero tomare los salones que salen en los nodos TEXT que si son los correctos, no trabaje con los nodos text porque encontre varias dificultades ahi en formatos y coordenadas
                informacion.pop()
                materia = informacion[0]
                try:
                    maestro = informacion[1]
                except:
                    maestro = ''
                salon = self.salones[j]

                self.clases.append({
                    'materia': materia,
                    'maestro': maestro,
                    'salon': salon,
                    'color': color,
                    'atributos': atributos
                })
                j += 1
            except:
                continue

        self.calendarioFormat()
        self.doc.unlink()
        return self.calendario


    def calendarioFormat(self):
        # Aqui es -2 en horarios porque recuperaremos siempre 2 textos de la utm [ El primero: es la direccion, El segundo: Validado mas la fecha ]
        # valor inicial de los cuadros en x = 345 como siempre son 6 mantiene la proporcion en X
        # Ancho de los cuadros = 513 como siempre son 6 mantiene la proporcion en X
        # valor inicial de los cuadros en y =  valueY[0]
        # Alto de los cuadros = height de rect
        # Por lo tanto tenemos que:
        #
        #                             513                    513
        #             ___________________________________________________
        #            |_______|________LU___________|_________MA__________| <---valorInicialY
        #            |7:00   |                     |                     |
        #  x = 345---------->|    height de rect-> |                     | <-height de rect
        #            |       |      MATE p TI      |     PROGRAMACION    |
        #             -------[^]----------------- ------------------------
        #                      y = valueY[0]
        #
        valueY = self.getValorInicialDeY()
        valorInicialY = valueY[1]
        self.calendario = [
            [str(345 + 513 * x) + ',' + str(valorInicialY + valueY[0] * y) for x in range(len(self.dias) - 1)] for y in
            range(len(self.horarios) - 2)
        ]
        i = 0
        j = 0
        cuadros_ocupados_por_la_materia = 0
        for row in self.calendario:
            for column in row:
                indexClass = 0
                for clase in self.clases:
                    try:
                        coordenadas = column.split(',')
                        p1 = float(clase['atributos']['x'])
                        p2 = float(clase['atributos']['y'])
                        c1 = float(coordenadas[0])
                        c2 = float(coordenadas[1])
                        if p1 == c1 and p2 <= c2:
                            cuadros_ocupados_por_la_materia = int(float(clase['atributos']['height']) / valueY[0])
                            if cuadros_ocupados_por_la_materia == 1:
                                self.calendario[i][j] = {
                                    'materia': clase['materia'],
                                    'maestro': clase['maestro'],
                                    'salon': clase['salon'],
                                    'color': clase['color']
                                } # [0]
                            else:
                                for x in range(cuadros_ocupados_por_la_materia):
                                    self.calendario[i + x][j]= {
                                        'materia': clase['materia'],
                                        'maestro': clase['maestro'],
                                        'salon': clase['salon'],
                                        'color': clase['color']
                                    } # [0]
                            self.clases.pop(indexClass)
                            break
                    except:
                        break
                    indexClass += 1
                j += 1
            i += 1
            j = 0
        self.calendario = self.deleteEspaciosEnBlanco(self.calendario)
        self.calendario = self.addHorasAndDias(self.calendario)

    def setHoras(self, item):
        if self.isHorario(item._attrs['x'].value):
            self.horarios.append({
                'item': item.childNodes[0].data,
                'atributos': [{'x': item._attrs['x'].value, 'y': item._attrs['y'].value}]
            })


    def setDias(self, item):
        self.dias.append(item.childNodes[0].data)

    def isHorario(self, x):
        if float(x) < float(self.referencia_de_x):
            return True
        return False

    def addHorasAndDias(self, calendario):
        i = 0
        for row in calendario:
            row.insert(0, self.horarios[i]['item'])
            i += 1
        calendario.insert(0, self.dias)
        return calendario

    def getValorInicialDeY(self):
        coordenadasX = []
        minY = 10000
        minSize = 10000
        row = []
        for clase in self.clases:
            coordenadasX.append(float(clase['atributos']['x']))
            if float(clase['atributos']['y']) < minY:
                minY = float(clase['atributos']['y'])
            if float(clase['atributos']['height']) < minSize:
                minSize = float(clase['atributos']['height'])

        row.append(minSize)
        row.append(minY)
        return row

    def deleteEspaciosEnBlanco(self, calendario):
        for i in range(len(calendario)):
            for j in range(len(calendario[i])):
                try:
                    coordenada = calendario[i][j].split(',')
                    if len(coordenada) > 1:
                        calendario[i][j] = {
                            'materia': 'modulo libre',
                            'maestro': '',
                            'salon': 'Lab X',
                            'color': '#FFFFFF'
                        }
                except:
                    continue
        return calendario

# obj = Calendario()