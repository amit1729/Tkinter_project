import customtkinter
from tkinter import *
import datetime
from functools import partial

class CreateSheet(customtkinter.CTkScrollableFrame):
    def __init__(self,master):
        super().__init__(master, label_text='Create Monthly Salary Report')
        self.grid(row=0, column=1,rowspan=4, padx=(20, 0), pady=(20,0), sticky="nsew")
        
        # self.grid_columnconfigure((1,4,6,8,10,13), weight = 2)
        # self.grid_columnconfigure(2, weight = 1)
        # self.grid_columnconfigure((3,5,7,9,11,12), weight = 3)
        x = 7
        y = 4
        z = 1
        self.grid_columnconfigure(1,weight =x)
        self.grid_columnconfigure(4,weight =x)
        self.grid_columnconfigure(6,weight =x)
        self.grid_columnconfigure(8,weight =x)
        self.grid_columnconfigure(10,weight =x)
        self.grid_columnconfigure(13,weight =x)

        self.grid_columnconfigure(3,weight =y)
        self.grid_columnconfigure(5,weight =y)
        self.grid_columnconfigure(7,weight =y)
        self.grid_columnconfigure(9,weight =y)
        self.grid_columnconfigure(11,weight =y)
        self.grid_columnconfigure(12,weight =y)

        self.grid_columnconfigure(2,weight =z)

        self.name = self._ctsv('Amit')
        self.dob = self._ctsv('22/10/2000')
        self.co = self._ctsv('fk No')
        self.rank = self._ctsv('radiant')
        self.mobno = self._ctsv('8888888888')
        self.basicPay = self._ctsv('200000')
        self.da = self._ctsv('20')
        self.tda = self._ctsv('20000')
        self.daontda = self._ctsv('20')
        self.deductions = self._ctsv('2000')
        self.hra = self._ctsv('10')
        
        self.entries = []
        self.index = 0
        today = datetime.date.today()

        self.dateLabel = customtkinter.CTkLabel(self, text="Create the Pay sheet for the month of: ", font=customtkinter.CTkFont(size=17, weight="bold"),anchor = 'w')
        self.dateLabel.grid(row = 0, column = 0 , columnspan = 6, padx=(20, 20), pady=(20,0), sticky = "ew")

        self.monthList = ['January', 'Febuary', 'March', 'April','May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        self.monthVar = StringVar(value=self.monthList[today.month-1])
        self.monthOptionMenu = customtkinter.CTkOptionMenu(self,values=self.monthList,variable=self.monthVar)
        self.monthOptionMenu.grid(row = 0, column = 8 , columnspan = 3, padx=(30, 20), pady=(20,0), sticky = "w")

        self.yearList = list(map(str, list(range(today.year-15,today.year+2,1))))
        self.yearVar = StringVar(value=str(today.year))
        self.yearOptionMenu = customtkinter.CTkOptionMenu(self,values=self.yearList,variable=self.yearVar)
        self.yearOptionMenu.grid(row = 0, column = 11 , columnspan = 3, padx=(20, 30), pady=(20,0), sticky = "e")

        self.snoEntry = customtkinter.CTkEntry(self, placeholder_text="Serial Number of Employee")
        self.snoEntry.grid(row = 1, column = 1 , columnspan = 6, padx=(20, 20), pady=(20,0), sticky = "ew")
        self.searchButton = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text='Search Employee', command=self.searchButtonClicked)
        self.searchButton.grid(row=1, column=8, columnspan = 6, padx=(20, 20), pady=(20, 0), sticky="ew")

    def _ctsv(self,x):
        return StringVar(value=str(x))
    
    def searchButtonClicked(self):
        self.textbox = customtkinter.CTkTextbox(master=self,height = 100, width = 150)
        self.textbox.grid(row=2, column=1, columnspan = 6,padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.textbox.insert('0.0', f'Name: {self.name.get()}\nDate of Birth: {self.dob.get()}\nCO: {self.co.get()}\nRank: {self.rank.get()}\nMobile Number: {self.mobno.get()}')
        self.textbox.configure(state = 'disabled')
        self.searchButton = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text='Add',height = 80, command=self.addButtonClicked)
        self.searchButton.grid(row=2, column=8, columnspan = 6, padx=(20, 20), pady=(20, 20), sticky="ew")

    def disable(self, widgt):
        widgt.configure(state = 'disable')

    def createRecord(self):
        record = [
                str(self.index),
                f'Name: {self.name.get()}\nDate of Birth: {self.dob.get()}\nCO: {self.co.get()}\nRank: {self.rank.get()}\nMobile Number: {self.mobno.get()}',
                  '8000000',
                  '20',
                  '200000',
                  '12',
                  '120000',
                  '12000',
                  '10',
                  '1200',
                  '12000',
                  '10000000'
                   ]
        return record

    def addButtonClicked(self):
        headers = ['S.No', 'Personal Details', 'Basic Pay','HRA(%)', 'HRA', 'DA%', 'DA', 'TDA', 'DA to TDA(%)', 'DA to TDA', 'Deductions', 'Total', 'Action']
        if self.index == 0:
            for i, header in enumerate(headers):
                self.ele = customtkinter.CTkEntry(self,corner_radius=0,font=customtkinter.CTkFont(size=11))
                self.ele.grid(row = self.index+3, column = i+1, sticky = 'snew')
                self.ele.insert(END, header)
                self.disable(self.ele)
        record = self.createRecord()
        elements = []
        for i, rec in enumerate(record):
            if i == 1:
                self.ele = customtkinter.CTkTextbox(master=self,height = 70,corner_radius=0,font=customtkinter.CTkFont(size=10))
                self.ele.grid(row=self.index+4, column=i+1, sticky="nsew")
                self.ele.insert(END,rec)
                elements.append(self.ele)
                self.disable(self.ele)
            else:
                self.ele = customtkinter.CTkEntry(master=self,corner_radius=0,font=customtkinter.CTkFont(size=10))
                self.ele.grid(row=self.index+4, column=i+1, sticky="nsew")
                self.ele.insert(END,rec)
                elements.append(self.ele)
                self.disable(self.ele)
        self.deleteButton = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2,bg_color='red', text_color=("gray10", "#DCE4EE"), text='Remove', command=partial(self.deleteButtonClicked, self.index),font=customtkinter.CTkFont(size=10, weight='bold'))
        self.deleteButton.grid(row=self.index+4, column=13, padx=(5, 5),pady = (5,5), sticky="nsew")
        elements.append(self.deleteButton)
        self.entries.append(elements)
        self.index+=1

    def deleteButtonClicked(self, i):
        for ele in self.entries[i]:
            ele.destroy()



        


    
