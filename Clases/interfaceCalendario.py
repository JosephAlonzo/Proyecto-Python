# from tkinter import *
# from tkinter import ttk

# from calendario import Calendario 
# from htmlRecuperator import HtmlRecuperator 
# from jsonConverter import jsonConverter

# class Application():
#     def __init__(self, root):
        # self.root = root
        # self.root.title("Calendario")
        # self.root.columnconfigure(0, weight=2)
        # self.root.rowconfigure(0, weight=2)

        # self.label = Label(self.root, text="Link")
        # self.label.grid(column=0, row=0)

        # self.content = StringVar()
        # self.txt = Entry(self.root, width=30, textvariable=self.content)
        # self.txt.grid(column=1, row = 0)
        # self.labelsArray = []
        # self.btn = Button(self.root, text="Enviar", command= lambda: self.makeTable() )
        # self.btn.grid(column = 2, row=0, columnspan=2)

        

    # def makeTable(self):
        # url = self.content.get()

        # htmlRecuperator = HtmlRecuperator(url)
        # svg = htmlRecuperator.getSvg()

        # calendarioUtm = Calendario(svg)
        # calendarioUtm = calendarioUtm.calendario
        # json = jsonConverter(calendarioUtm)
        # json.convertArrayToJSON()

        # row = len(calendarioUtm.calendario)
        # column = len(calendarioUtm.calendario[0])
        # self.labelsArray = []
        # self.labelsArray = [ [ "" for x in range(column) ] for y in range(row) ]

        # index = 0
        # rowWeight = 1
        # for j in range(column):
            # for i in range(row):
            #     if(i == 0 or j == 0):
            #         value = calendarioUtm.calendario[i][j]
            #         color = '#FFF'
            #     else:
            #         try:
            #             value = calendarioUtm.calendario[i][j][0] + '\n' +calendarioUtm.calendario[i][j][1]+ '\n' + calendarioUtm.calendario[i][j][2] 
            #         except:
            #             try:
            #                 value = calendarioUtm.calendario[i][j][0] + '\n' +calendarioUtm.calendario[i][j][1]
            #             except:
            #                 value=""
            #         try:
            #             color = calendarioUtm.calendario[i][j][3]['color']
            #         except:
            #             color = '#FFF'
            #         # try:
            #         #     if value == calendarioUtm.calendario[i+1][j][0]:
            #         #         rowWeight+=1
            #         #         continue
            #         # except:
            #         #     rowWeight = 1
                        
            #     self.labelsArray[i][j] = Label(self.root, text= value, bg=color, borderwidth=1, relief="solid")
            #     self.labelsArray[i][j].grid(row=i+1, column=j, sticky="nsew", ipadx=10, ipady=15)
            #     self.root.columnconfigure(j, weight=1)
            #     index += i
            #     self.root.rowconfigure(index , weight=rowWeight)
            #     rowWeight = 1
            # index = 0

    
            
# main_window = Tk()
# app = Application(main_window)
# main_window.mainloop()


from tkinter import Button, Tk, HORIZONTAL

from tkinter.ttk import Progressbar
import time
import threading

class MonApp(Tk):
    def __init__(self):
        super().__init__()


        self.btn = Button(self, text='Traitement', command=self.traitement)
        self.btn.grid(row=0,column=0)
        self.progress = Progressbar(self, orient=HORIZONTAL,length=100,  mode='indeterminate')


    def traitement(self):
        def real_traitement():
            self.progress.grid(row=1,column=0)
            self.progress.start()
            time.sleep(5)
            self.progress.stop()
            self.progress.grid_forget()

            self.btn['state']='normal'

        self.btn['state']='disabled'
        threading.Thread(target=real_traitement).start()

if __name__ == '__main__':

    app = MonApp()
    app.mainloop()