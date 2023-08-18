import customtkinter
from tkinter import *

class UpdatePersonal(customtkinter.CTkScrollableFrame):
    def __init__(self,master,connection):
        super().__init__(master, label_text='Update Personal Details')
        self.con = connection
        self.grid(row=0, column=1,rowspan=4, padx=(20, 0), pady=(20,0), sticky="nsew")
        self.grid_columnconfigure((1,2,4), weight = 1)
        self.grid_columnconfigure(3, weight = 2)
        self.snoEntry = customtkinter.CTkEntry(self, placeholder_text="Serial Number of Employee To Update")
        self.snoEntry.grid(row = 0, column = 2, padx=(20, 20), pady=(20,0), sticky = "ew")
        self.searchButton = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text='Search Employee', command=self.searchButtonClicked)
        self.searchButton.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="w")

    def _ctsv(self,x):
        return StringVar(value=str(x))
    
    def searchButtonClicked(self):
        self.name = self._ctsv('Amit')
        self.dob = self._ctsv('22/10/2000')
        self.co = self._ctsv('fk No')
        self.rank = self._ctsv('radiant')
        self.mobno = self._ctsv('8888888888')

        self.nameLabel = customtkinter.CTkLabel(self, text="Name: ", font=customtkinter.CTkFont(size=15, weight="bold"), anchor ='w')
        self.nameLabel.grid(row = 1, column = 2, padx=(20, 20), pady=(20,0), sticky = "ew")
        self.nameEntry = customtkinter.CTkEntry(self, placeholder_text="Name", textvariable=self.name)
        self.nameEntry.grid(row = 1, column = 3, padx=(20, 20), pady=(20,0), sticky = "ew")

        self.rankLabel = customtkinter.CTkLabel(self, text="Rank: ", font=customtkinter.CTkFont(size=15, weight="bold"),anchor = 'w')
        self.rankLabel.grid(row = 2, column = 2, padx=(20, 20), pady=(20,0), sticky = "ew")
        self.rankEntry = customtkinter.CTkEntry(self, placeholder_text="Rank", textvariable=self.rank)
        self.rankEntry.grid(row = 2, column = 3, padx=(20, 20), pady=(20,0), sticky = "ew")

        self.mobnoLabel = customtkinter.CTkLabel(self, text="Mobile Number: ", font=customtkinter.CTkFont(size=15, weight="bold"),anchor = 'w')
        self.mobnoLabel.grid(row = 3, column = 2, padx=(20, 20), pady=(20,0), sticky = "ew")
        self.mobnoEntry = customtkinter.CTkEntry(self, placeholder_text="Mobile Number", textvariable=self.mobno)
        self.mobnoEntry.grid(row = 3, column = 3, padx=(20, 20), pady=(20,0), sticky = "ew")

        self.dobLabel = customtkinter.CTkLabel(self, text="Date of Birth: ", font=customtkinter.CTkFont(size=15, weight="bold"),anchor = 'w')
        self.dobLabel.grid(row = 4, column = 2, padx=(20, 20), pady=(20,0), sticky = "ew")
        self.dobEntry = customtkinter.CTkEntry(self, placeholder_text="DD/MM/YYYY", textvariable=self.dob)
        self.dobEntry.grid(row = 4, column = 3, padx=(20, 20), pady=(20,0), sticky = "ew")

        self.coLabel = customtkinter.CTkLabel(self, text="CO: ", font=customtkinter.CTkFont(size=15, weight="bold"),anchor = 'w')
        self.coLabel.grid(row = 5, column = 2, padx=(20, 20), pady=(20,0), sticky = "ew")
        self.coEntry = customtkinter.CTkEntry(self, placeholder_text="CO", textvariable=self.co)
        self.coEntry.grid(row = 5, column = 3, padx=(20, 20), pady=(20,0), sticky = "ew")

        self.nextButton = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text='Next', command=self.nextButtonClicked)
        self.nextButton.grid(row=6, column=3, padx=(20, 20), pady=(20, 20), sticky="w")

        self.clearButton = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text='Clear',command=self.clearButtonClicked)
        self.clearButton.grid(row=6, column=2, padx=(20, 20), pady=(20, 20), sticky="e")

    

    def nextButtonClicked(self):
        self.nextButton.destroy()
        self.clearButton.destroy()
        self.nameEntry.configure(state = 'disabled')
        self.rankEntry.configure(state = 'disabled')
        self.mobnoEntry.configure(state = 'disabled')
        self.coEntry.configure(state = 'disabled')
        self.dobEntry.configure(state = 'disabled')
        self.submitButton = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text='Submit', command=self.submitButtonClicked)
        self.submitButton.grid(row=6, column=3, padx=(20, 20), pady=(20, 0), sticky="w")

        self.editButton = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text='Edit', command=self.editButtonClicked)
        self.editButton.grid(row=6, column=2, padx=(20, 20), pady=(20, 0), sticky="e")

        self.msgLabel = customtkinter.CTkLabel(self, text="*Please Confirm the Details!", font=customtkinter.CTkFont(size=10, weight="bold"), anchor ='w',text_color='red')
        self.msgLabel.grid(row = 7, column = 1,columnspan = 4, padx=(20, 20), pady=(20,0), sticky = "ew")
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
        self.nextButton.grid(row=6, column=3, padx=(20, 20), pady=(20, 20), sticky="w")

        self.clearButton = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text='Clear',command=self.clearButtonClicked)
        self.clearButton.grid(row=6, column=2, padx=(20, 20), pady=(20, 20), sticky="e")
        self.msgLabel.destroy()

    def clearButtonClicked(self):
        self.nameEntry.delete(0,'end')
        self.rankEntry.delete(0,'end')
        self.mobnoEntry.delete(0,'end')
        self.coEntry.delete(0,'end')
        self.dobEntry.delete(0,'end')

    def submitButtonClicked(self):
        self.destroy()
        # self.master.current = UpdateSalary(self.master, 0)
