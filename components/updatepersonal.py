import customtkinter
from tkinter import *
from tkinter import messagebox
from .utils import validDate, validNumber, chageFormat, log_errors_to_file
from functools import partial

@log_errors_to_file('out/errorlogs.txt')
class UpdatePersonal(customtkinter.CTkScrollableFrame):
    def __init__(self,master,connection):
        super().__init__(master, label_text='Update Personal Details')
        self.con = connection
        self.grid(row=0, column=1,rowspan=4, padx=(20, 0), pady=(20,0), sticky="nsew")
        self.grid_columnconfigure((1,2,4), weight = 1)
        self.grid_columnconfigure(3, weight = 2)
        self.idEntry = customtkinter.CTkEntry(self, placeholder_text="Employee Number of Employee To Update")
        self.idEntry.grid(row = 0, column = 2, padx=(20, 20), pady=(20,0), sticky = "ew")
        self.searchButton = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text='Search Employee', command=self.searchButtonClicked)
        self.searchButton.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="w")
        self.idEntry.bind('<Return>', command=self.enterPressed)

    @log_errors_to_file('out/errorlogs.txt')
    def enterPressed(self,event):
        self.searchButtonClicked()

    @log_errors_to_file('out/errorlogs.txt')
    def _ctsv(self,x):
        return StringVar(value=str(x))
    
    @log_errors_to_file('out/errorlogs.txt')
    def fetchPersonalDetails(self):
        cur = self.con.cursor()
        res = cur.execute("SELECT * FROM Personal WHERE id = ?",
               (self.idEntry.get(),))
        row = res.fetchone()
        cur.close()
        flag = not row == None
        return row, flag
    
    @log_errors_to_file('out/errorlogs.txt')
    def searchButtonClicked(self):
        data, exists = self.fetchPersonalDetails()
        if exists:
            self.id = self.idEntry.get()
            self.name = self._ctsv(data[1])
            self.rank = self._ctsv(data[2])
            self.postedat = self._ctsv(data[3])
            self.citycode = self._ctsv(data[4])
            self.doj = self._ctsv(chageFormat(data[5], '%Y-%m-%d','%d/%m/%Y' ))
            self.doi = self._ctsv(chageFormat(data[6], '%Y-%m-%d','%d/%m/%Y' ))
            self.pran = self._ctsv(data[7])

            self.nameLabel = customtkinter.CTkLabel(self, text="Name: ", font=customtkinter.CTkFont(size=15, weight="bold"), anchor ='w')
            self.nameLabel.grid(row = 1, column = 2, padx=(20, 20), pady=(30,0), sticky = "ew")
            self.nameEntry = customtkinter.CTkEntry(self, placeholder_text="Name", textvariable=self.name)
            self.nameEntry.grid(row = 1, column = 3, padx=(20, 20), pady=(30,0), sticky = "ew")

            self.rankLabel = customtkinter.CTkLabel(self, text="Rank: ", font=customtkinter.CTkFont(size=15, weight="bold"),anchor = 'w')
            self.rankLabel.grid(row = 2, column = 2, padx=(20, 20), pady=(10,0), sticky = "ew")
            self.rankEntry = customtkinter.CTkEntry(self, placeholder_text="Rank", textvariable=self.rank)
            self.rankEntry.grid(row = 2, column = 3, padx=(20, 20), pady=(10,0), sticky = "ew")

            self.postedatLabel = customtkinter.CTkLabel(self, text="Posted At: ", font=customtkinter.CTkFont(size=15, weight="bold"),anchor = 'w')
            self.postedatLabel.grid(row = 3, column = 2, padx=(20, 20), pady=(10,0), sticky = "ew")
            self.postedatEntry = customtkinter.CTkEntry(self, placeholder_text="Station", textvariable=self.postedat)
            self.postedatEntry.grid(row = 3, column = 3, padx=(20, 20), pady=(10,0), sticky = "ew")

            self.citycodeLabel = customtkinter.CTkLabel(self, text="City Code: ", font=customtkinter.CTkFont(size=15, weight="bold"),anchor = 'w')
            self.citycodeLabel.grid(row = 4, column = 2, padx=(20, 20), pady=(10,0), sticky = "ew")
            self.citycodeEntry = customtkinter.CTkEntry(self, placeholder_text="City Code", textvariable=self.citycode)
            self.citycodeEntry.grid(row = 4, column = 3, padx=(20, 20), pady=(10,0), sticky = "ew")

            self.dojLabel = customtkinter.CTkLabel(self, text="DOJ: ", font=customtkinter.CTkFont(size=15, weight="bold"),anchor = 'w')
            self.dojLabel.grid(row = 5, column = 2, padx=(20, 20), pady=(10,0), sticky = "ew")
            self.dojEntry = customtkinter.CTkEntry(self, placeholder_text="DD/MM/YYYY", textvariable=self.doj)
            self.dojEntry.grid(row = 5, column = 3, padx=(20, 20), pady=(10,0), sticky = "ew")

            self.doiLabel = customtkinter.CTkLabel(self, text="DOI: ", font=customtkinter.CTkFont(size=15, weight="bold"),anchor = 'w')
            self.doiLabel.grid(row = 6, column = 2, padx=(20, 20), pady=(10,0), sticky = "ew")
            self.doiEntry = customtkinter.CTkEntry(self, placeholder_text="DD/MM/YYYY", textvariable=self.doi)
            self.doiEntry.grid(row = 6, column = 3, padx=(20, 20), pady=(10,0), sticky = "ew")

            self.pranLabel = customtkinter.CTkLabel(self, text="PRAN: ", font=customtkinter.CTkFont(size=15, weight="bold"),anchor = 'w')
            self.pranLabel.grid(row = 7, column = 2, padx=(20, 20), pady=(10,0), sticky = "ew")
            self.pranEntry = customtkinter.CTkEntry(self, placeholder_text="PRAN", textvariable=self.pran)
            self.pranEntry.grid(row = 7, column = 3, padx=(20, 20), pady=(10,0), sticky = "ew")

            self.nextButton = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text='Next', command=self.nextButtonClicked)
            self.nextButton.grid(row=8, column=3, padx=(20, 20), pady=(20, 20), sticky="w")

            self.clearButton = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text='Clear',command=self.clearButtonClicked)
            self.clearButton.grid(row=8, column=2, padx=(20, 20), pady=(20, 20), sticky="e")

        else:
            messagebox.showerror('Error', f'Empolyee with serial number {self.idEntry.get()} does not exists')

    @log_errors_to_file('out/errorlogs.txt')
    def validationError(self, wdgt, msg):
        # self.editButtonClicked()
        wdgt.focus()
        messagebox.showerror('Input Error',  msg)

    @log_errors_to_file('out/errorlogs.txt')
    def validate(self, data):
        if not validNumber(data['id'][0]):
            self.validationError(data['id'][1], 'Please enter a valid employee ID')
            return False
        elif len(data['name'][0]) == 0:
            self.validationError(data['name'][1], 'Please enter the name of the employee')
            return False
        elif len(data['rank'][0]) == 0:
            self.validationError(data['rank'][1], 'Please enter the rank of the employee')
            return False
        elif len(data['postedat'][0]) == 0:
            self.validationError(data['postedat'][1], 'Please enter the posting station of the employee')
            return False
        elif len(data['citycode'][0]) == 0:
            self.validationError(data['citycode'][1], 'Please enter the city code')
            return False
        elif not validDate(data['doj'][0]):
            self.validationError(data['doj'][1], 'Please enter a valid date in dd/mm/yyyy format')
            return False
        elif not validDate(data['doi'][0]):
            self.validationError(data['doi'][1], 'Please enter a valid date in dd/mm/yyyy format')
            return False
        elif not validNumber(data['pran'][0]):
            self.validationError(data['pran'][1], 'Please enter PRAN number of the employee')
            return False
        return True

    @log_errors_to_file('out/errorlogs.txt')
    def nextButtonClicked(self):
        self.data = {}
        self.data['name'] = (self.nameEntry.get(), self.nameEntry)
        self.data['rank'] = (self.rankEntry.get(), self.rankEntry)
        self.data['id'] = (self.idEntry.get(), self.idEntry)
        self.data['postedat'] = (self.postedatEntry.get(), self.postedatEntry)
        self.data['citycode'] = (self.citycodeEntry.get(), self.citycodeEntry)
        self.data['doj'] = (self.dojEntry.get(), self.dojEntry)
        self.data['doi'] = (self.doiEntry.get(), self.doiEntry)
        self.data['pran'] = (self.pranEntry.get(), self.pranEntry)
        if self.validate(self.data):
            self.nextButton.destroy()
            self.clearButton.destroy()
            self.nameEntry.configure(state = 'disabled')
            self.idEntry.configure(state = 'disabled')
            self.rankEntry.configure(state = 'disabled')
            self.postedatEntry.configure(state = 'disabled')
            self.citycodeEntry.configure(state = 'disabled')
            self.dojEntry.configure(state = 'disabled')
            self.doiEntry.configure(state = 'disabled')
            self.pranEntry.configure(state = 'disabled')
            self.submitButton = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text='Submit', command=self.submitButtonClicked)
            self.submitButton.grid(row=8, column=3, padx=(20, 20), pady=(20, 0), sticky="w")

            self.editButton = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text='Edit', command=self.editButtonClicked)
            self.editButton.grid(row=8, column=2, padx=(20, 20), pady=(20, 0), sticky="e")

            self.msgLabel = customtkinter.CTkLabel(self, text="*Please Confirm the Details!", font=customtkinter.CTkFont(size=10, weight="bold"), anchor ='w',text_color='red')
            self.msgLabel.grid(row = 9, column = 1,columnspan = 4, padx=(20, 20), pady=(20,0), sticky = "ew")
            # messagebox.showinfo('Confirm Details', 'Please confirm the Employee Details')

    @log_errors_to_file('out/errorlogs.txt')
    def editButtonClicked(self):
        self.submitButton.destroy()
        self.editButton.destroy()
        self.idEntry.configure(state = 'normal')
        self.nameEntry.configure(state = 'normal')
        self.rankEntry.configure(state = 'normal')
        self.postedatEntry.configure(state = 'normal')
        self.citycodeEntry.configure(state = 'normal')
        self.dojEntry.configure(state = 'normal')
        self.doiEntry.configure(state = 'normal')
        self.pranEntry.configure(state = 'normal')
        self.nextButton = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text='Next', command=self.nextButtonClicked)
        self.nextButton.grid(row=8, column=3, padx=(20, 20), pady=(20, 20), sticky="w")

        self.clearButton = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text='Clear',command=self.clearButtonClicked)
        self.clearButton.grid(row=8, column=2, padx=(20, 20), pady=(20, 20), sticky="e")
        self.msgLabel.destroy()

    @log_errors_to_file('out/errorlogs.txt')
    def clearButtonClicked(self):
        self.idEntry.delete(0,'end')
        self.nameEntry.delete(0,'end')
        self.rankEntry.delete(0,'end')
        self.postedatEntry.delete(0,'end')
        self.citycodeEntry.delete(0,'end')
        self.dojEntry.delete(0,'end')
        self.doiEntry.delete(0,'end')
        self.pranEntry.delete(0,'end')

    @log_errors_to_file('out/errorlogs.txt')
    def submitButtonClicked(self):
        cur = self.con.cursor()
        cur.execute("UPDATE Personal SET name = ?, rank = ?, postedat = ?, citycode = ?, doj = ?, doi = ?, pran = ? WHERE id = ?",
            (self.data['name'][0],
             self.data['rank'][0],
             self.data['postedat'][0],
             self.data['citycode'][0],
             chageFormat(self.data['doj'][0], '%d/%m/%Y', '%Y-%m-%d'),
             chageFormat(self.data['doi'][0], '%d/%m/%Y', '%Y-%m-%d'),
             self.data['pran'][0],
             self.id))
        self.con.commit()
        cur.close()
        messagebox.showinfo('Success',  f'Details of Employee with id \'{self.id}\' Updated Successfully')
        # self.destroy()
        # self.master.current = UpdateSalary(self.master, 0)
        self.idEntry.configure(state = 'normal')
        destList = [self.nameLabel, self.nameEntry, self.rankLabel, self.rankEntry,
                    self.postedatEntry, self.postedatLabel, self.citycodeEntry, self.citycodeLabel,
                    self.dojEntry, self.dojLabel, self.doiEntry, self.doiLabel, self.pranEntry, self.pranLabel,
                     self.submitButton, self.editButton, self.msgLabel,
                    ]
        for ele in destList:
            try:
                ele.destroy()
            except:
                pass
