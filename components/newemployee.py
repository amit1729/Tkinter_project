import customtkinter
from .updatesal import UpdateSalary
from tkinter import messagebox
from .utils import validDate, validNumber, chageFormat

class NewEmp(customtkinter.CTkScrollableFrame):
    def __init__(self,master,connection):
        super().__init__(master, label_text='New Employee`s Details', label_font=customtkinter.CTkFont(size=18, weight="bold"))
        self.master=master
        self.con = connection
        self.grid(row=0, column=1,rowspan=4, padx=(20, 0), pady=(20,0), sticky="nsew")
        self.grid_columnconfigure((1,2,4), weight = 1)
        self.grid_columnconfigure(3, weight = 2)

        self.nameLabel = customtkinter.CTkLabel(self, text="Name: ", font=customtkinter.CTkFont(size=15, weight="bold"), anchor ='w')
        self.nameLabel.grid(row = 0, column = 2, padx=(20, 20), pady=(20,0), sticky = "ew")
        self.nameEntry = customtkinter.CTkEntry(self, placeholder_text="Name")
        self.nameEntry.grid(row = 0, column = 3, padx=(20, 20), pady=(20,0), sticky = "ew")

        self.rankLabel = customtkinter.CTkLabel(self, text="Rank: ", font=customtkinter.CTkFont(size=15, weight="bold"),anchor = 'w')
        self.rankLabel.grid(row = 1, column = 2, padx=(20, 20), pady=(20,0), sticky = "ew")
        self.rankEntry = customtkinter.CTkEntry(self, placeholder_text="Rank")
        self.rankEntry.grid(row = 1, column = 3, padx=(20, 20), pady=(20,0), sticky = "ew")

        self.mobnoLabel = customtkinter.CTkLabel(self, text="Mobile Number: ", font=customtkinter.CTkFont(size=15, weight="bold"),anchor = 'w')
        self.mobnoLabel.grid(row = 2, column = 2, padx=(20, 20), pady=(20,0), sticky = "ew")
        self.mobnoEntry = customtkinter.CTkEntry(self, placeholder_text="Mobile Number")
        self.mobnoEntry.grid(row = 2, column = 3, padx=(20, 20), pady=(20,0), sticky = "ew")

        self.dobLabel = customtkinter.CTkLabel(self, text="Date of Birth: ", font=customtkinter.CTkFont(size=15, weight="bold"),anchor = 'w')
        self.dobLabel.grid(row = 3, column = 2, padx=(20, 20), pady=(20,0), sticky = "ew")
        self.dobEntry = customtkinter.CTkEntry(self, placeholder_text="DD/MM/YYYY")
        self.dobEntry.grid(row = 3, column = 3, padx=(20, 20), pady=(20,0), sticky = "ew")

        self.coLabel = customtkinter.CTkLabel(self, text="CO: ", font=customtkinter.CTkFont(size=15, weight="bold"),anchor = 'w')
        self.coLabel.grid(row = 4, column = 2, padx=(20, 20), pady=(20,0), sticky = "ew")
        self.coEntry = customtkinter.CTkEntry(self, placeholder_text="CO")
        self.coEntry.grid(row = 4, column = 3, padx=(20, 20), pady=(20,0), sticky = "ew")

        self.nextButton = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text='Next', command=self.nextButtonClicked)
        self.nextButton.grid(row=5, column=3, padx=(20, 20), pady=(20, 20), sticky="w")

        self.clearButton = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text='Clear',command=self.clearButtonClicked)
        self.clearButton.grid(row=5, column=2, padx=(20, 20), pady=(20, 20), sticky="e")

    

    def nextButtonClicked(self):
        self.data = {}
        self.data['name'] = (self.nameEntry.get(), self.nameEntry)
        self.data['rank'] = (self.rankEntry.get(), self.rankEntry)
        self.data['dob'] = (self.dobEntry.get(), self.dobEntry)
        self.data['co'] = (self.coEntry.get(), self.coEntry)
        self.data['mobno'] = (self.mobnoEntry.get(), self.mobnoEntry)
        if self.validate(self.data):
            self.nextButton.destroy()
            self.clearButton.destroy()
            self.nameEntry.configure(state = 'disabled')
            self.rankEntry.configure(state = 'disabled')
            self.mobnoEntry.configure(state = 'disabled')
            self.coEntry.configure(state = 'disabled')
            self.dobEntry.configure(state = 'disabled')
            self.submitButton = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text='Submit', command=self.submitButtonClicked)
            self.submitButton.grid(row=5, column=3, padx=(20, 20), pady=(20, 20), sticky="w")

            self.editButton = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text='Edit', command=self.editButtonClicked)
            self.editButton.grid(row=5, column=2, padx=(20, 20), pady=(20, 20), sticky="e")

            self.msgLabel = customtkinter.CTkLabel(self, text="*Please Confirm the Details!", font=customtkinter.CTkFont(size=10, weight="bold"), anchor ='w',text_color='red')
            self.msgLabel.grid(row = 6, column = 1,columnspan = 4, padx=(20, 20), pady=(20,0), sticky = "ew")
        # messagebox.showinfo('Confirm Details', 'Please confirm the Employee Details')


    def editButtonClicked(self):
        self.submitButton.destroy()
        self.editButton.destroy()
        self.nameEntry.configure(state = 'normal')
        self.rankEntry.configure(state = 'normal')
        self.mobnoEntry.configure(state = 'normal')
        self.coEntry.configure(state = 'normal')
        self.dobEntry.configure(state = 'normal')
        self.nextButton = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text='Next', command=self.nextButtonClicked)
        self.nextButton.grid(row=5, column=3, padx=(20, 20), pady=(20, 20), sticky="w")

        self.clearButton = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text='Clear',command=self.clearButtonClicked)
        self.clearButton.grid(row=5, column=2, padx=(20, 20), pady=(20, 20), sticky="e")
        self.msgLabel.destroy()

    def clearButtonClicked(self):
        self.nameEntry.delete(0,'end')
        self.rankEntry.delete(0,'end')
        self.mobnoEntry.delete(0,'end')
        self.coEntry.delete(0,'end')
        self.dobEntry.delete(0,'end')

    def validationError(self, wdgt, msg):
        # self.editButtonClicked()
        wdgt.focus()
        messagebox.showerror('Input Error',  msg)


    def validate(self, data):
        if len(data['name'][0]) == 0:
            self.validationError(data['name'][1], 'Please enter the name of the employee')
            return False
        elif len(data['rank'][0]) == 0:
            self.validationError(data['rank'][1], 'Please enter the rank of the employee')
            return False
        elif not validNumber(data['mobno'][0]):
            self.validationError(data['mobno'][1], 'Please enter a valid 10 digit mobile number')
            return False
        elif not validDate(data['dob'][0]):
            self.validationError(data['dob'][1], 'Please enter a valid date in dd/mm/yyyy format')
            return False
        elif len(data['co'][0]) == 0:
            self.validationError(data['co'][1], 'Please enter the CO`s name of the employee')
            return False
        return True

    def unique(self):
        cur = self.con.cursor()
        res = cur.execute("SELECT * FROM Personal WHERE name = ? and dob = ? and co = ? and rank = ? and mobno = ?",
               (self.data['name'][0].upper(), chageFormat(self.data['dob'][0], '%d/%m/%Y', '%Y-%m-%d'), self.data['co'][0].upper(), self.data['rank'][0].upper(), self.data['mobno'][0]))
        rows = res.fetchall()
        cur.close()
        if len(rows) == 0:
            return True
        else: return False

    def submitButtonClicked(self):
        if self.unique():
            cur = self.con.cursor()
            cur.execute("INSERT INTO Personal (name, dob, co, rank, mobno) VALUES (?, ?, ?, ?, ?)",
                (self.data['name'][0].upper(), chageFormat(self.data['dob'][0], '%d/%m/%Y', '%Y-%m-%d'), self.data['co'][0].upper(), self.data['rank'][0].upper(), self.data['mobno'][0]))
            sno = cur.lastrowid
            self.con.commit()
            cur.close()
            self.destroy()
            self.master.current = UpdateSalary(self.master,self.con, sno)
        else:
            messagebox.showinfo('Error',  'Empoyee already exists')
            self.editButtonClicked()

        
        


