import customtkinter
from tkinter import *
import tkinter as tk
from tkinter import messagebox
from .utils import chageFormat


class DisplaySheet(customtkinter.CTkScrollableFrame):
    def __init__(self,master,connection):

        self.sallis=[]
        self.des(self.sallis)
        self.row0 = 0
        super().__init__(master, label_text='Employee Details')
        self.con = connection
        cur = (self.con).cursor()
        self.grid(row=self.row0, column=1,rowspan=4, padx=(20, 0), pady=(20,0), sticky="nsew")
        
        self.row0=self.row0+1
        self.search_results=[]

        Employee_table=cur.execute("SELECT * FROM Personal")

        self.snoEntry = customtkinter.CTkEntry(self, placeholder_text="S.No./Name/Rank of the Employee")
        self.snoEntry.grid(row = self.row0, column = 1 , columnspan = 3, padx=(5, 20), pady=(10,20), sticky = "ew")
        self.searchButton = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text='Search Employee', command=self.searchButtonClicked)
        self.searchButton.grid(row=self.row0, column=4, columnspan = 1, padx=(5, 20), pady=(10, 20), sticky="ew")
        self.snoEntry.bind('<Return>', command=self.enterPressed)

        self.row0=self.row0+1
        self.index_table=[self.searchButton,self.snoEntry]
        s1=["S.No.","Name","Rank","Mobile Number","Date of Birth","CO","Salary"]
        self.w=[60,200,60,100,120,200,80]

        for i in range(len(s1)):

            self.Labels = customtkinter.CTkTextbox(master=self,height = 40,corner_radius=1,font=customtkinter.CTkFont(size=17),width=self.w[i])
            self.Labels.grid(row = self.row0, column = i+1,padx=5, pady=5, sticky = "nsew")
            self.Labels.insert(END,s1[i])
            self.index_table.append(self.Labels)

        j=self.row0
        self.main_table=[]
        for i in Employee_table:
            j=j+1
            f=1
            s=[i[0],i[1],i[4],i[5],i[2],i[3]]
            for k in s:
                self.printdetails = customtkinter.CTkTextbox(master=self,height = 40,corner_radius=1,font=customtkinter.CTkFont(size=15),width=self.w[f-1])
                self.printdetails.grid(row = j, column = f,padx=5, pady=5, sticky = "nsew")
                self.printdetails.insert(END,k)
                self.main_table.append(self.printdetails)
                f=f+1

            self.printdetails = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text='Salary', command=lambda sno=i[0]: self.salarybuttonclicked(sno))
            self.printdetails.grid(row = j, column = f, columnspan = 1,padx=5, pady=5, sticky = "nsew")
            self.main_table.append(self.printdetails)
            f=f+1

        cur.close()

    def enterPressed(self,event):
        self.searchButtonClicked()

    def searchButtonClicked(self):

        self.des(self.main_table)
        self.des(self.search_results)

        cur = (self.con).cursor()
        Employee_tables = cur.execute("SELECT * FROM Personal WHERE name LIKE ? OR id = ? OR rank = ?",('%'+self.snoEntry.get()+'%',self.snoEntry.get(),self.snoEntry.get(),))
        row=Employee_tables.fetchall()
        exists = not len(row) == 0

        if exists:
            j1=2

            for i in row:
                j1=j1+1
                f=1
                s=[i[0],i[1],i[4],i[5],i[2],i[3]]

                for k in s:
                    self.printdetails = customtkinter.CTkTextbox(master=self,height = 40,corner_radius=1,font=customtkinter.CTkFont(size=15),width=self.w[f-1])
                    self.printdetails.grid(row = j1, column = f, padx=5 , pady=5, sticky = "nsew")
                    self.printdetails.insert(END,k)
                    f=f+1
                    self.search_results.append(self.printdetails)
                
                self.printdetails = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text='Salary', command=lambda sno=i[0]: self.salarybuttonclicked(sno))
                self.printdetails.grid(row = j1, column = f, columnspan = 1,padx=5, pady=5, sticky = "nsew")
                self.search_results.append(self.printdetails)
                f=f+1

        else:
            messagebox.showerror('Not Found', f'Empolyee with S.No./Name/Rank {self.snoEntry.get()} does not exists')

        cur.close()
        
    def salarybuttonclicked(self,sno):
        self.des(self.main_table)
        self.des(self.index_table)
        self.des(self.search_results)
        cur = (self.con).cursor()
        row=cur.execute('SELECT Personal.id,Personal.name,Personal.mobno,Salary.basic,Salary.da,Salary.tda,Salary.hra FROM Salary INNER JOIN Personal ON Salary.id = Personal.id WHERE Salary.id = ? ',(sno,))
        salary_row=row.fetchone()
        if salary_row   != None :

            s=["S.No.","Name","Mobile Number","Basic","DA","TDA","HRA"]
            self.w=[60,200,150,120,120,120,120]

            for i in range(len(s)):

                self.labels = customtkinter.CTkTextbox(master=self,height = 40,corner_radius=1,font=customtkinter.CTkFont(size=17),width=self.w[i])
                self.labels.grid(row = self.row0, column = i+1,padx=5, pady=5, sticky = "nsew")
                self.labels.insert(END,s[i])
                self.sallis.append(self.labels)

            j1=3
            f=1
            s=[salary_row[0],salary_row[1],salary_row[2],salary_row[3],salary_row[4],salary_row[5],salary_row[6]]

            for k in s:
                self.PrintDetails = customtkinter.CTkTextbox(master=self,height = 40,corner_radius=1,font=customtkinter.CTkFont(size=15),width=self.w[f-1])
                self.PrintDetails.grid(row = j1, column = f, padx=5 , pady=5, sticky = "nsew")
                self.PrintDetails.insert(END,k)
                f=f+1
                self.search_results.append(self.PrintDetails)
                self.sallis.append(self.PrintDetails)
            
        else:
            messagebox.showerror('Not Found', f'Salary details of Empolyee with S.No. {sno} do not exist')

        cur.close()

    
    def _ctsv(self,x):
        return StringVar(value=str(x))
    
    def des(self,l):
        for i in l:
            i.destroy()
        l.clear()

