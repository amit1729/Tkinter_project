import customtkinter
from tkinter import *
from tkinter import messagebox
import datetime
from .utils import validAmount, validPercent, chageFormat
from functools import partial

class UpdateSalary(customtkinter.CTkScrollableFrame):
    def __init__(self,master,connection, sno = ''):
        super().__init__(master, label_text='Update Salary')
        self.master = master
        self.con = connection
        self.grid(row=0, column=1,rowspan=4, padx=(20, 0), pady=(20,0), sticky="nsew")
        self.grid_columnconfigure((1,2,4), weight = 1)
        self.grid_columnconfigure(3, weight = 2)
        # Dictionary with id as key and a tuple as value (label widget, button widget)
        self.startRow = 0
        self.snoDict = {}
        today = datetime.date.today()
        self.monthList = ['January', 'Febuary', 'March', 'April','May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        self.monthVar = StringVar(value=self.monthList[today.month-1])

        self.yearList = list(map(str, list(range(today.year-15,today.year+2,1))))
        self.yearVar = StringVar(value=str(today.year))
        self.dateLabel = customtkinter.CTkLabel(self, text="Month/Year of Salary: ", font=customtkinter.CTkFont(size=15, weight="bold"),anchor = 'w')
        self.dateLabel.grid(row = 0, column = 2, padx=(20, 20), pady=(20,0), sticky = "ew")

        self.monthOptionMenu = customtkinter.CTkOptionMenu(self,values=self.monthList,variable=self.monthVar)
        self.monthOptionMenu.grid(row = 0, column = 3, padx=(30, 20), pady=(20,0), sticky = "w")

        self.yearOptionMenu = customtkinter.CTkOptionMenu(self,values=self.yearList,variable=self.yearVar)
        self.yearOptionMenu.grid(row = 0, column = 3, padx=(20, 30), pady=(20,0), sticky = "e")

        self.paramLabel = customtkinter.CTkLabel(self, text="Parameters to Update: ", font=customtkinter.CTkFont(size=15, weight="bold"), anchor ='w')
        self.paramLabel.grid(row = 1, column = 2, padx=(20, 20), pady=(20,0), sticky = "ew")
        self.paramVar = IntVar(value=0)
        self.paramAllRB = customtkinter.CTkRadioButton(self,text='All', value=0, variable=self.paramVar, command=self.paramRBEvent)
        self.paramAllRB.grid(row = 1, column = 3, padx=(20, 20), pady=(20,0), sticky = 'w')
        self.paramCustomRB = customtkinter.CTkRadioButton(self,text='Custom', value=1, variable=self.paramVar, command=self.paramRBEvent)
        self.paramCustomRB.grid(row = 1, column = 3, padx=(20, 20), pady=(20,0), sticky = 'e')

        self.recordsLabel = customtkinter.CTkLabel(self, text="Records to Update: ", font=customtkinter.CTkFont(size=15, weight="bold"), anchor ='w')
        self.recordsLabel.grid(row = 3, column = 2, padx=(20, 20), pady=(20,0), sticky = "ew")
        self.recordsVar = IntVar(value=0)
        self.recordsAllRB = customtkinter.CTkRadioButton(self,text='All', value=0, variable=self.recordsVar, command=self.recordsRBEvent)
        self.recordsAllRB.grid(row = 3, column = 3, padx=(20, 20), pady=(20,0), sticky = 'w')
        self.recordsCustomRB = customtkinter.CTkRadioButton(self,text='Custom', value=1, variable=self.recordsVar, command=self.recordsRBEvent)
        self.recordsCustomRB.grid(row = 3, column = 3, padx=(20, 20), pady=(20,0), sticky = 'e')
        # self.height = 0
        self.gmcVar = StringVar(value='14')
        self.indvcVar = StringVar(value='10')
        self.basicLabel = customtkinter.CTkLabel(self, text="Basic Pay: ", font=customtkinter.CTkFont(size=15, weight="bold"), anchor ='w')
        self.basicEntry = customtkinter.CTkEntry(self, placeholder_text="Enter Basic Pay")
        self.daLabel = customtkinter.CTkLabel(self, text="DA: ", font=customtkinter.CTkFont(size=15, weight="bold"), anchor ='w')
        self.daEntry = customtkinter.CTkEntry(self, placeholder_text="Enter Dearness allowance(%)")
        self.tptLabel = customtkinter.CTkLabel(self, text="TPT: ", font=customtkinter.CTkFont(size=15, weight="bold"), anchor ='w')
        self.tptEntry = customtkinter.CTkEntry(self, placeholder_text="Enter TPT")
        self.hraLabel = customtkinter.CTkLabel(self, text="HRA: ", font=customtkinter.CTkFont(size=15, weight="bold"), anchor ='w')
        self.hraEntry = customtkinter.CTkEntry(self, placeholder_text="Enter HRA(%)")
        self.gmcLabel = customtkinter.CTkLabel(self, text="GMC: ", font=customtkinter.CTkFont(size=15, weight="bold"), anchor ='w')
        self.gmcEntry = customtkinter.CTkEntry(self, textvariable = self.gmcVar)
        self.indvcLabel = customtkinter.CTkLabel(self, text="Individual Contribution: ", font=customtkinter.CTkFont(size=15, weight="bold"), anchor ='w')
        self.indvcEntry = customtkinter.CTkEntry(self, textvariable = self.indvcVar)
        self.cgeisLabel = customtkinter.CTkLabel(self, text="CGEIS: ", font=customtkinter.CTkFont(size=15, weight="bold"), anchor ='w')
        self.cgeisEntry = customtkinter.CTkOptionMenu(self,values=['0','30','45','60'])

        self.basicLabel.grid(row = 6, column = 2, padx=(20, 20), pady=(20,0), sticky = "ew")
        self.basicEntry.grid(row = 6, column = 3, padx=(20, 20), pady=(10,0), sticky = "ew")
        self.daLabel.grid(row = 7, column = 2, padx=(20, 20), pady=(10,0), sticky = "ew")
        self.daEntry.grid(row = 7, column = 3, padx=(20, 20), pady=(10,0), sticky = "ew")
        self.tptLabel.grid(row = 8, column = 2, padx=(20, 20), pady=(10,0), sticky = "ew")
        self.tptEntry.grid(row = 8, column = 3, padx=(20, 20), pady=(10,0), sticky = "ew")
        self.hraLabel.grid(row = 9, column = 2, padx=(20, 20), pady=(10,0), sticky = "ew")
        self.hraEntry.grid(row = 9, column = 3, padx=(20, 20), pady=(10,0), sticky = "ew")
        self.gmcLabel.grid(row = 10, column = 2, padx=(20, 20), pady=(10,0), sticky = "ew")
        self.gmcEntry.grid(row = 10, column = 3, padx=(20, 20), pady=(10,0), sticky = "ew")
        self.indvcLabel.grid(row = 11, column = 2, padx=(20, 20), pady=(10,0), sticky = "ew")
        self.indvcEntry.grid(row = 11, column = 3, padx=(20, 20), pady=(10,0), sticky = "ew")
        self.cgeisLabel.grid(row = 12, column = 2, padx=(20, 20), pady=(10,0), sticky = "ew")
        self.cgeisEntry.grid(row = 12, column = 3, padx=(20, 20), pady=(10,0), sticky = "ew")

    def cbEvent(self, idx):
        if self.params[idx][4].get():
            self.params[idx][1].grid(row = self.params[idx][3], column = 3, padx=(20, 20), pady=(10,0), sticky = "ew")
            self.params[idx][2].grid(row = self.params[idx][3], column = 2, padx=(20, 20), pady=(10,0), sticky = "ew")
        else:
            self.params[idx][1].grid_forget()
            self.params[idx][2].grid_forget()

    def paramRBEvent(self):
        if self.paramVar.get():
            self.basicLabel.grid_forget()
            self.basicEntry.grid_forget()
            self.daLabel.grid_forget()
            self.daEntry.grid_forget()
            self.tptLabel.grid_forget()
            self.tptEntry.grid_forget()
            self.hraLabel.grid_forget()
            self.hraEntry.grid_forget()
            self.gmcLabel.grid_forget()
            self.gmcEntry.grid_forget()
            self.indvcLabel.grid_forget()
            self.indvcEntry.grid_forget()
            self.cgeisLabel.grid_forget()
            self.cgeisEntry.grid_forget()

            self.params = {
                'basic': ['Basic Pay', self.basicEntry, self.basicLabel,6],
                'da': ['DA(%)', self.daEntry,self.daLabel,7],
                'tpt': ['TPT', self.tptEntry, self.tptLabel,8],
                'hra': ['HRA(%)',self.hraEntry, self.hraLabel,9],
                'gmc': ['GMC(%)',self.gmcEntry,self.gmcLabel,10],
                'indvc': ['INDV Contri',self.indvcEntry,self.indvcLabel,11],
                'cgeis': ['CGEIS',self.cgeisEntry,self.cgeisLabel,12]
            }
            self.cbFrame = customtkinter.CTkFrame(self,fg_color='#333333')
            self.cbFrame.grid(row = 2, column = 2,columnspan = 2, pady=(20,0), sticky = '')
            for i,p in enumerate(self.params.keys()):
                self.cb = customtkinter.CTkCheckBox(self.cbFrame, text=self.params[p][0], onvalue=1, offvalue=0, checkbox_height=20, checkbox_width=20, command=partial(self.cbEvent,p))
                if i//4 == 0:
                    self.cb.grid(row = i//4, column = i%4, padx=(15, 15), pady=(10,10), sticky = 'w')
                else:
                    self.cb.grid(row = i//4, column = i%4, padx=(15, 15), pady=(0,10), sticky = 'w')
                self.params[p].append(self.cb)
        else:
            self.cbFrame.destroy()
            self.basicLabel.grid(row = 6, column = 2, padx=(20, 20), pady=(20,0), sticky = "ew")
            self.basicEntry.grid(row = 6, column = 3, padx=(20, 20), pady=(10,0), sticky = "ew")
            self.daLabel.grid(row = 7, column = 2, padx=(20, 20), pady=(10,0), sticky = "ew")
            self.daEntry.grid(row = 7, column = 3, padx=(20, 20), pady=(10,0), sticky = "ew")
            self.tptLabel.grid(row = 8, column = 2, padx=(20, 20), pady=(10,0), sticky = "ew")
            self.tptEntry.grid(row = 8, column = 3, padx=(20, 20), pady=(10,0), sticky = "ew")
            self.hraLabel.grid(row = 9, column = 2, padx=(20, 20), pady=(10,0), sticky = "ew")
            self.hraEntry.grid(row = 9, column = 3, padx=(20, 20), pady=(10,0), sticky = "ew")
            self.gmcLabel.grid(row = 10, column = 2, padx=(20, 20), pady=(10,0), sticky = "ew")
            self.gmcEntry.grid(row = 10, column = 3, padx=(20, 20), pady=(10,0), sticky = "ew")
            self.indvcLabel.grid(row = 11, column = 2, padx=(20, 20), pady=(10,0), sticky = "ew")
            self.indvcEntry.grid(row = 11, column = 3, padx=(20, 20), pady=(10,0), sticky = "ew")
            self.cgeisLabel.grid(row = 12, column = 2, padx=(20, 20), pady=(10,0), sticky = "ew")
            self.cgeisEntry.grid(row = 12, column = 3, padx=(20, 20), pady=(10,0), sticky = "ew")

    def getResults(self):
        # Returns list of unique ids with string to display attached (id, string to display)
        # pass
        self.snoEntry.delete(0,END)
        return [(1, '1: Amit Kumar Yadav'), (2, 'Ajeer'), (3, 'damit'), (4, 'sasas')]
    
    def recordsRBEvent(self):
        if self.recordsVar.get():
            self.infoFrame = customtkinter.CTkScrollableFrame(self)
            self.infoFrame.grid(row = 5, column = 2,columnspan = 2, padx=(20, 20), pady=(20,0), sticky = 'ew')
            self.snoEntry = customtkinter.CTkEntry(self, placeholder_text="Serial Number of Employees To Update")
            self.snoEntry.grid(row = 4, column = 2,columnspan =2, padx=(20, 20), pady=(20,0), sticky = "ew")
            self.snoEntry.bind('<Return>', command=self.enterPressed)
        else:
            self.infoFrame.grid_forget()
            self.snoEntry.destroy()

    def enterPressed(self,event):
        rec = self.getResults()
        for r in rec:
            label = customtkinter.CTkLabel(self.infoFrame, text=r[1], font=customtkinter.CTkFont(size=14,weight='bold', family='arial'), corner_radius=6, fg_color="#333333", padx = 15)
            label.grid(row = self.startRow//2, column = 2*(self.startRow%2), padx=(20,5), pady=(10,0), sticky = 'ew')
            button = customtkinter.CTkButton(self.infoFrame, text='X',fg_color="gray10", border_width=2, text_color='white', width=28, font=customtkinter.CTkFont(size=14,weight='bold', family='arial'), command=partial(self.deleteButtonClicked, r[0]))
            button.grid(row = self.startRow//2, column = 2*(self.startRow%2)+1, padx=(0, 20), pady=(10,0), sticky = 'w')
          
            self.snoDict[r[0]] = (label, button)
            self.startRow+=1

    def deleteButtonClicked(self, i):
        self.snoDict[i][0].destroy()
        self.snoDict[i][1].destroy()
        del self.snoDict[i]

        

