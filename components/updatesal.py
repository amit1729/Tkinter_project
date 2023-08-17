import customtkinter
from tkinter import *
import datetime

class UpdateSalary(customtkinter.CTkScrollableFrame):
    def __init__(self,master, sno = 1):
        super().__init__(master, label_text='Update Salary')
        self.grid(row=0, column=1,rowspan=4, padx=(20, 0), pady=(20,0), sticky="nsew")
        self.grid_columnconfigure((1,2,4), weight = 1)
        self.grid_columnconfigure(3, weight = 2)
        self.serialNumber = StringVar(value=str(sno))
        self.snoEntry = customtkinter.CTkEntry(self, placeholder_text="Serial Number of Employee To Update", textvariable=self.serialNumber)
        self.snoEntry.grid(row = 0, column = 2, padx=(20, 20), pady=(20,0), sticky = "ew")
        self.searchButton = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text='Search Employee', command=self.searchButtonClicked)
        self.searchButton.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="w")
        if self.serialNumber.get()!="":
            self.snoEntry.configure(state="disabled")
            self.searchButton.configure(state="disabled")
            self.searchButtonClicked()
        

    def _ctsv(self,x):
        return StringVar(value=str(x))
    
    def searchButtonClicked(self):
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

        self.nameLabel = customtkinter.CTkLabel(self, text="Name: ", font=customtkinter.CTkFont(size=15, weight="bold"), anchor ='w')
        self.nameLabel.grid(row = 1, column = 2, padx=(20, 20), pady=(20,0), sticky = "ew")
        self.nameEntry = customtkinter.CTkEntry(self, placeholder_text="Name", textvariable=self.name)
        self.nameEntry.grid(row = 1, column = 3, padx=(20, 20), pady=(20,0), sticky = "ew")
        self.nameEntry.configure(state="disabled")

        self.rankLabel = customtkinter.CTkLabel(self, text="Rank: ", font=customtkinter.CTkFont(size=15, weight="bold"),anchor = 'w')
        self.rankLabel.grid(row = 2, column = 2, padx=(20, 20), pady=(20,0), sticky = "ew")
        self.rankEntry = customtkinter.CTkEntry(self, placeholder_text="Rank", textvariable=self.rank)
        self.rankEntry.grid(row = 2, column = 3, padx=(20, 20), pady=(20,0), sticky = "ew")
        self.rankEntry.configure(state="disabled")

        self.mobnoLabel = customtkinter.CTkLabel(self, text="Mobile Number: ", font=customtkinter.CTkFont(size=15, weight="bold"),anchor = 'w')
        self.mobnoLabel.grid(row = 3, column = 2, padx=(20, 20), pady=(20,0), sticky = "ew")
        self.mobnoEntry = customtkinter.CTkEntry(self, placeholder_text="Mobile Number", textvariable=self.mobno)
        self.mobnoEntry.grid(row = 3, column = 3, padx=(20, 20), pady=(20,0), sticky = "ew")
        self.mobnoEntry.configure(state="disabled")

        self.dobLabel = customtkinter.CTkLabel(self, text="Date of Birth: ", font=customtkinter.CTkFont(size=15, weight="bold"),anchor = 'w')
        self.dobLabel.grid(row = 4, column = 2, padx=(20, 20), pady=(20,0), sticky = "ew")
        self.dobEntry = customtkinter.CTkEntry(self, placeholder_text="DD/MM/YYYY", textvariable=self.dob)
        self.dobEntry.grid(row = 4, column = 3, padx=(20, 20), pady=(20,0), sticky = "ew")
        self.dobEntry.configure(state="disabled")

        self.coLabel = customtkinter.CTkLabel(self, text="CO: ", font=customtkinter.CTkFont(size=15, weight="bold"),anchor = 'w')
        self.coLabel.grid(row = 5, column = 2, padx=(20, 20), pady=(20,0), sticky = "ew")
        self.coEntry = customtkinter.CTkEntry(self, placeholder_text="CO", textvariable=self.co)
        self.coEntry.grid(row = 5, column = 3, padx=(20, 20), pady=(20,0), sticky = "ew")
        self.coEntry.configure(state="disabled")

        today = datetime.date.today()

        self.dateLabel = customtkinter.CTkLabel(self, text="Month/Year of Salary: ", font=customtkinter.CTkFont(size=15, weight="bold"),anchor = 'w')
        self.dateLabel.grid(row = 6, column = 2, padx=(20, 20), pady=(20,0), sticky = "ew")

        self.monthList = ['January', 'Febuary', 'March', 'April','May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        self.monthVar = StringVar(value=self.monthList[today.month-1])
        self.monthOptionMenu = customtkinter.CTkOptionMenu(self,values=self.monthList,variable=self.monthVar)
        self.monthOptionMenu.grid(row = 6, column = 3, padx=(30, 20), pady=(20,0), sticky = "w")

        self.yearList = list(map(str, list(range(today.year-15,today.year+2,1))))
        self.yearVar = StringVar(value=str(today.year))
        self.yearOptionMenu = customtkinter.CTkOptionMenu(self,values=self.yearList,variable=self.yearVar)
        self.yearOptionMenu.grid(row = 6, column = 3, padx=(20, 30), pady=(20,0), sticky = "e")

        self.basicLabel = customtkinter.CTkLabel(self, text="Basic Pay: ", font=customtkinter.CTkFont(size=15, weight="bold"),anchor = 'w')
        self.basicLabel.grid(row = 7, column = 2, padx=(20, 20), pady=(20,0), sticky = "ew")
        self.basicEntry = customtkinter.CTkEntry(self, placeholder_text="Basic Pay", textvariable=self.basicPay)
        self.basicEntry.grid(row = 7, column = 3, padx=(20, 20), pady=(20,0), sticky = "ew")

        self.daLabel = customtkinter.CTkLabel(self, text="Dearness Allowance(%): ", font=customtkinter.CTkFont(size=15, weight="bold"),anchor = 'w')
        self.daLabel.grid(row = 8, column = 2, padx=(20, 20), pady=(20,0), sticky = "ew")
        self.daEntry = customtkinter.CTkEntry(self, placeholder_text="10", textvariable=self.da)
        self.daEntry.grid(row = 8, column = 3, padx=(20, 20), pady=(20,0), sticky = "ew")

        self.tdaLabel = customtkinter.CTkLabel(self, text="TDA: ", font=customtkinter.CTkFont(size=15, weight="bold"),anchor = 'w')
        self.tdaLabel.grid(row = 9, column = 2, padx=(20, 20), pady=(20,0), sticky = "ew")
        self.tdaEntry = customtkinter.CTkEntry(self, placeholder_text="10", textvariable=self.tda)
        self.tdaEntry.grid(row = 9, column = 3, padx=(20, 20), pady=(20,0), sticky = "ew")

        self.daontdaLabel = customtkinter.CTkLabel(self, text="DA on TDA: ", font=customtkinter.CTkFont(size=15, weight="bold"),anchor = 'w')
        self.daontdaLabel.grid(row = 10, column = 2, padx=(20, 20), pady=(20,0), sticky = "ew")
        self.daontdaEntry = customtkinter.CTkEntry(self, placeholder_text="10", textvariable=self.daontda)
        self.daontdaEntry.grid(row = 10, column = 3, padx=(20, 20), pady=(20,0), sticky = "ew")

        self.deductionsLabel = customtkinter.CTkLabel(self, text="Deductions: ", font=customtkinter.CTkFont(size=15, weight="bold"),anchor = 'w')
        self.deductionsLabel.grid(row = 11, column = 2, padx=(20, 20), pady=(20,0), sticky = "ew")
        self.deductionsEntry = customtkinter.CTkEntry(self, placeholder_text="10", textvariable=self.deductions)
        self.deductionsEntry.grid(row = 11, column = 3, padx=(20, 20), pady=(20,0), sticky = "ew")

        self.hraLabel = customtkinter.CTkLabel(self, text="HRA: ", font=customtkinter.CTkFont(size=15, weight="bold"),anchor = 'w')
        self.hraLabel.grid(row = 12, column = 2, padx=(20, 20), pady=(20,0), sticky = "ew")
        self.hraEntry = customtkinter.CTkEntry(self, placeholder_text="10", textvariable=self.hra)
        self.hraEntry.grid(row = 12, column = 3, padx=(20, 20), pady=(20,0), sticky = "ew")

        self.nextButton = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text='Next', command=self.nextButtonClicked)
        self.nextButton.grid(row=13, column=3, padx=(20, 20), pady=(20, 20), sticky="w")

        self.clearButton = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text='Clear',command=self.clearButtonClicked)
        self.clearButton.grid(row=13, column=2, padx=(20, 20), pady=(20, 20), sticky="e")

    def nextButtonClicked(self):
        self.nextButton.destroy()
        self.clearButton.destroy()
        self.basicEntry.configure(state = 'disabled')
        self.daEntry.configure(state = 'disabled')
        self.tdaEntry.configure(state = 'disabled')
        self.daontdaEntry.configure(state = 'disabled')
        self.deductionsEntry.configure(state = 'disabled')
        self.hraEntry.configure(state = 'disabled')
        self.submitButton = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text='Submit', command=self.submitButtonClicked)
        self.submitButton.grid(row=11, column=3, padx=(20, 20), pady=(20, 0), sticky="w")

        self.editButton = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text='Edit', command=self.editButtonClicked)
        self.editButton.grid(row=11, column=2, padx=(20, 20), pady=(20, 0), sticky="e")

        self.msgLabel = customtkinter.CTkLabel(self, text="*Please Confirm the Details!", font=customtkinter.CTkFont(size=10, weight="bold"), anchor ='w',text_color='red')
        self.msgLabel.grid(row = 12, column = 1,columnspan = 4, padx=(20, 20), pady=(0,0), sticky = "ew")
        # messagebox.showinfo('Confirm Details', 'Please confirm the Employee Details')


    def editButtonClicked(self):
        self.submitButton.destroy()
        self.editButton.destroy()
        self.basicEntry.configure(state = 'normal')
        self.daEntry.configure(state = 'normal')
        self.tdaEntry.configure(state = 'normal')
        self.daontdaEntry.configure(state = 'normal')
        self.deductionsEntry.configure(state = 'normal')
        self.hraEntry.configure(state = 'normal')
        self.nextButton = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text='Next', command=self.nextButtonClicked)
        self.nextButton.grid(row=11, column=3, padx=(20, 20), pady=(20, 20), sticky="w")

        self.clearButton = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text='Clear',command=self.clearButtonClicked)
        self.clearButton.grid(row=11, column=2, padx=(20, 20), pady=(20, 20), sticky="e")
        self.msgLabel.destroy()

    def clearButtonClicked(self):
        self.basicEntry.delete(0,'end')
        self.daEntry.delete(0,'end')
        self.tdaEntry.delete(0,'end')
        self.daontdaEntry.delete(0,'end')
        self.deductionsEntry.delete(0,'end')
        self.hraEntry.delete(0,'end')

    def submitButtonClicked(self):
        self.destroy()
        # self.master.current = UpdateSalary(self.master, 0)




