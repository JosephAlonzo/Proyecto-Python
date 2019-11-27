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


# from tkinter import Button, Tk, HORIZONTAL

# from tkinter.ttk import Progressbar
# import time
# import threading

# class MonApp(Tk):
#     def __init__(self):
#         super().__init__()


#         self.btn = Button(self, text='Traitement', command=self.traitement)
#         self.btn.grid(row=0,column=0)
#         self.progress = Progressbar(self, orient=HORIZONTAL,length=100,  mode='indeterminate')


#     def traitement(self):
#         def real_traitement():
#             self.progress.grid(row=1,column=0)
#             self.progress.start()
#             time.sleep(5)
#             self.progress.stop()
#             self.progress.grid_forget()

#             self.btn['state']='normal'

#         self.btn['state']='disabled'
#         threading.Thread(target=real_traitement).start()

# if __name__ == '__main__':

#     app = MonApp()
#     app.mainloop()


# from tkinter import *

# master = Tk()

# scrollbar = Scrollbar(master)
# scrollbar.pack(side=RIGHT, fill=Y)

# listbox = Listbox(master, yscrollcommand=scrollbar.set)
# for i in range(1000):
#     listbox.insert(END, str(i))
# listbox.pack(side=LEFT, fill=BOTH)

# scrollbar.config(command=listbox.yview)

# mainloop()

from tkinter import *
from tkinter import ttk

name_list = ('George', 'Maria', 'Peter', 'Nick')
surname_list = ('Lycos', 'Ntou', 'Wolf', 'Stath')
telephone_list = ('6950 123123', '6950 123456', '6951 025458', '6970 985214')
root = Tk()
root.title('Treeview')
root.configure(background='Yellow Green')

ttk.Label(root, text='There must be colors at some rows:', font=('DejaVu Sans', 11, 'bold'), background= 'yellow green').grid(row=0, column=0)
tree = ttk.Treeview(root, columns=('name', 'surname', 'telephone'))
tree.grid(row=1, column=0)
ttk.Button(root, text='Exit', command=root.destroy).grid(row=3, column=0, pady=10)
tree.heading('#0', text='Α/Α')
tree.heading('name', text='Name')
tree.heading('surname', text='Surname')
tree.heading('telephone', text='Telephone')

tree.column('#0', width=50)
tree.column('telephone', anchor='center')

for i, (name, surname, telephone) in enumerate(zip(name_list, surname_list, telephone_list), start=1):
    if i % 2 != 0:
        tree.insert(parent='', index='end', iid=str(i), text=str(i), values=(name, surname, telephone))
    else:
        tree.insert(parent='', index='end', iid=str(i), text=str(i), tags = 'paint', values=(name, surname, telephone))

tree.tag_configure(tagname='paint', background='yellow2')
root.mainloop()