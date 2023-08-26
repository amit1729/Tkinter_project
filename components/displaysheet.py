import customtkinter
from tkinter import *
import tkinter as tk
import datetime
from tkinter import messagebox
from .utils import chageFormat


class DisplaySheet(customtkinter.CTkScrollableFrame):
    def __init__(self,master,connection):

        self.sallis=[]
        self.id_current=[]
        self.search_results=[]
        self.main_table=[]
        self.index_table=[]
        self.des(self.sallis)
        self.row0 = 0
        super().__init__(master, label_text='Employee Details')
        self.con = connection
        cur = (self.con).cursor()
        self.grid(row=self.row0, column=1,rowspan=4, padx=(20, 0), pady=(20,0), sticky="nsew")

        self.grid_columnconfigure((1,2,4), weight = 1)
        self.grid_columnconfigure(3, weight = 2)
        
        self.row0=self.row0+0

        self.dateLabel = customtkinter.CTkLabel(self, text="Search the pay sheet for the month of: ", font=customtkinter.CTkFont(size=17, weight="bold"),anchor = 'w')
        self.dateLabel.grid(row = self.row0, column = 1 , columnspan = 2, padx=(10, 20), pady=(5,10), sticky = "ew")

        today = datetime.date.today()

        self.monthList = ['January', 'February', 'March', 'April','May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        self.monthVar = StringVar(value=self.monthList[today.month-1])
        self.monthOptionMenu = customtkinter.CTkOptionMenu(self,values=self.monthList,variable=self.monthVar)
        self.monthOptionMenu.grid(row = self.row0, column = 3 , columnspan = 1, padx=(10, 20), pady=(5,10), sticky = "w")

        self.yearList = list(map(str, list(range(today.year-15,today.year+2,1))))
        self.yearVar = StringVar(value=str(today.year))
        self.yearOptionMenu = customtkinter.CTkOptionMenu(self,values=self.yearList,variable=self.yearVar)
        self.yearOptionMenu.grid(row = self.row0, column = 4 , columnspan = 1, padx=(10, 20), pady=(5,10), sticky = "w")

        self.row0=self.row0+1

        Employee_table=cur.execute("SELECT * FROM Personal")

        self.snoEntry = customtkinter.CTkEntry(self, placeholder_text="Per No./Name/Rank of the Employee")
        self.snoEntry.grid(row = self.row0, column = 1 , columnspan = 2, padx=(20, 20), pady=(10,20), sticky = "ew")

        self.searchButton = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), 
                                                    text='Search Employee', command=self.searchButtonClicked)
        self.searchButton.grid(row=self.row0, column=3, columnspan = 1, padx=(5, 20), pady=(10, 20), sticky="ew")
        self.snoEntry.bind('<Return>', command=self.enterPressed)

        self.salaryButton = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), 
                                                    text='Show Salary', command= lambda: self.showbuttonclicked(self.id_current))
        self.salaryButton.grid(row=self.row0, column=4, columnspan = 1, padx=(5, 20), pady=(10, 20), sticky="ew")

        self.tableFrame = customtkinter.CTkScrollableFrame(self,corner_radius=0,orientation='horizontal')
        self.tableFrame.grid(row=self.row0+1, column=1,columnspan = 4, pady=(10,0), sticky="nsew")

        self.height=60
        self.tableFrame.configure(height = self.height)



        self.row0=self.row0+1
        self.index_table=[self.searchButton,self.snoEntry,self.salaryButton]
        s1=["Per No.","Name","Rank","Postedat","Citycode","DOJ","DOI","PRAN","Salary"]
        self.w=[80,200,60,100,100,150,150,150,80]

        
        for i in range(len(s1)):

            self.Labels = customtkinter.CTkTextbox(master=self.tableFrame,height = 40,corner_radius=1,font=customtkinter.CTkFont(size=17),
                                                   width=self.w[i])
            self.Labels.grid(row = self.row0, column = i+1,padx=5, pady=5, sticky = "nsew")
            self.Labels.insert(END,s1[i])
            self.index_table.append(self.Labels)

        j=self.row0

        for i in Employee_table:
            j=j+1
            f=1

            self.height+=60
            self.tableFrame.configure(height = self.height)

            self.id_current.append(i[0])

            for k in i:
                self.printdetails = customtkinter.CTkTextbox(master=self.tableFrame,height = 40,corner_radius=1,
                                                             font=customtkinter.CTkFont(size=15),width=self.w[f-1])
                self.printdetails.grid(row = j, column = f,padx=5, pady=5, sticky = "nsew")
                self.printdetails.insert(END,k)
                self.main_table.append(self.printdetails)
                f=f+1

            self.printdetails = customtkinter.CTkButton(master=self.tableFrame, fg_color="transparent", border_width=2, 
                                                        text_color=("gray10", "#DCE4EE"), text='Salary', 
                                                        command=lambda sno=i[0]: self.salarybuttonclicked(sno))
            self.printdetails.grid(row = j, column = f, columnspan = 1,padx=5, pady=5, sticky = "nsew")
            self.main_table.append(self.printdetails)
            f=f+1

        cur.close()

    def enterPressed(self,event):
        self.searchButtonClicked()

    def searchButtonClicked(self):
        self.id_current=[]
        self.height=60
        self.tableFrame.configure(height = self.height)

        self.des(self.main_table)
        self.des(self.search_results)

        cur = (self.con).cursor()
        Employee_tables = cur.execute("SELECT * FROM Personal WHERE UPPER(name) LIKE ? OR id = ? OR UPPER(rank) = ?",
                                      ('%'+str.upper(self.snoEntry.get())+'%',self.snoEntry.get(),str.upper(self.snoEntry.get()),))
        row=Employee_tables.fetchall()
        exists = not len(row) == 0

        if exists:
            j1=2

            for i in row:
                j1=j1+1
                f=1

                self.height+=60
                self.tableFrame.configure(height = self.height)
                self.id_current.append(i[0])

                for k in i:
                    self.printdetails = customtkinter.CTkTextbox(master=self.tableFrame,height = 40,corner_radius=1,
                                                                 font=customtkinter.CTkFont(size=15),width=self.w[f-1])
                    self.printdetails.grid(row = j1, column = f, padx=5 , pady=5, sticky = "nsew")
                    self.printdetails.insert(END,k)
                    f=f+1
                    self.search_results.append(self.printdetails)
                
                self.printdetails = customtkinter.CTkButton(master=self.tableFrame, fg_color="transparent", border_width=2, 
                                                            text_color=("gray10", "#DCE4EE"), text='Salary', 
                                                            command=lambda sno=i[0]: self.salarybuttonclicked(sno))
                self.printdetails.grid(row = j1, column = f, columnspan = 1,padx=5, pady=5, sticky = "nsew")
                self.search_results.append(self.printdetails)
                f=f+1

        else:
            messagebox.showerror('Not Found', f'Empolyee with S.No./Name/Rank {self.snoEntry.get()} does not exists')

        cur.close()
        
    def salarybuttonclicked(self,sno):

        month_num={
                "JANUARY": "01",
                "FEBRUARY": "02",
                "MARCH": "03",
                "APRIL": "04",
                "MAY": "05",
                "JUNE": "06",
                "JULY": "07",
                "AUGUST": "08",
                "SEPTEMBER": "09",
                "OCTOBER": "10",
                "NOVEMBER": "11",
                "DECEMBER": "12"
            }

        cur = (self.con).cursor()
        queryy=("SELECT Personal.id, Personal.name, Salary.basic, Salary.da, Salary.tpt, Salary.gmc, Salary.indvc, Salary.cgeis, Salary.hra FROM Salary INNER JOIN Personal ON Salary.id = Personal.id WHERE Salary.id = ? AND strftime('%m', Salary.date) = ? AND strftime('%Y', Salary.date) = ?")
        search_query=[sno,month_num.get(self.monthOptionMenu.get().upper()),self.yearOptionMenu.get()]
        row=cur.execute(queryy,search_query)

        

        #cur = (self.con).cursor()
        #row=cur.execute("SELECT Personal.id, Personal.name, Salary.basic, Salary.da, Salary.tpt, Salary.gmc, Salary.indvc, Salary.cgeis, Salary.hra FROM Salary INNER JOIN Personal ON Salary.id = Personal.id WHERE Salary.id = ? ",(sno,))   
        salary_row=row.fetchall()

        if len(salary_row) != 0 :

            self.des([self.dateLabel,self.monthOptionMenu,self.yearOptionMenu])
            self.des(self.main_table)
            self.des(self.index_table)
            self.des(self.search_results)

            self.height=60
            self.tableFrame.configure(height = self.height)

            s=["Per No.","Name","Basic","DA","TPT","GMC","INDVC","CGEIS","HRA"]
            self.w=[80,200,150,120,120,120,120,120,120]

            for i in range(len(s)):

                self.labels = customtkinter.CTkTextbox(master=self.tableFrame,height = 40,corner_radius=1,
                                                       font=customtkinter.CTkFont(size=17),width=self.w[i])
                self.labels.grid(row = self.row0, column = i+1,padx=5, pady=5, sticky = "nsew")
                self.labels.insert(END,s[i])
                self.sallis.append(self.labels)

            j1=2

            for sal_details in salary_row:

                self.height+=60
                self.tableFrame.configure(height = self.height)
                f=1
                j1=j1+1

                for k in sal_details:
                    self.PrintDetails = customtkinter.CTkTextbox(master=self.tableFrame,height = 40,corner_radius=1,
                                                                 font=customtkinter.CTkFont(size=15),width=self.w[f-1])
                    self.PrintDetails.grid(row = j1, column = f, padx=5 , pady=5, sticky = "nsew")
                    self.PrintDetails.insert(END,k)
                    f=f+1
                    self.search_results.append(self.PrintDetails)
                    self.sallis.append(self.PrintDetails)
            
        else:
            messagebox.showerror('Not Found', f'Salary details of Empolyee with S.No. {sno} do not exist')
            return

        cur.close()


    def showbuttonclicked(self,sno):

        #self.height=60
        #self.tableFrame.configure(height = self.height)

        month_num={
                "JANUARY": "01",
                "FEBRUARY": "02",
                "MARCH": "03",
                "APRIL": "04",
                "MAY": "05",
                "JUNE": "06",
                "JULY": "07",
                "AUGUST": "08",
                "SEPTEMBER": "09",
                "OCTOBER": "10",
                "NOVEMBER": "11",
                "DECEMBER": "12"
            }

        cur = (self.con).cursor()
        queryy=("SELECT Personal.id, Personal.name, Salary.basic, Salary.da, Salary.tpt, Salary.gmc, Salary.indvc, Salary.cgeis, Salary.hra FROM Salary INNER JOIN Personal ON Salary.id = Personal.id WHERE Salary.id IN ({}) AND strftime('%m', Salary.date) = ? AND strftime('%Y', Salary.date) = ?".format(", ".join(["?"] * len(sno))))
        search_query=sno
        search_query.append(month_num.get(self.monthOptionMenu.get().upper()))
        search_query.append(self.yearOptionMenu.get())
        row=cur.execute(queryy,search_query)


        salary_row=row.fetchall()

        if len(salary_row) != 0 :

            self.des(self.main_table)
            self.des(self.index_table)
            self.des(self.search_results)
            self.des([self.dateLabel,self.monthOptionMenu,self.yearOptionMenu])

            self.height=60
            self.tableFrame.configure(height = self.height)

            s=["Per No.","Name","Basic","DA","TPT","GMC","INDVC","CGEIS","HRA"]
            self.w=[80,200,150,120,120,120,120,120,120]

            for i in range(len(s)):

                self.labels = customtkinter.CTkTextbox(master=self.tableFrame,height = 40,corner_radius=1,
                                                       font=customtkinter.CTkFont(size=17),width=self.w[i])
                self.labels.grid(row = self.row0, column = i+1,padx=5, pady=5, sticky = "nsew")
                self.labels.insert(END,s[i])
                self.sallis.append(self.labels)

            j1=2

            for sal_details in salary_row:

                self.height+=60
                self.tableFrame.configure(height = self.height)
                f=1
                j1=j1+1

                for k in sal_details:
                    self.PrintDetails = customtkinter.CTkTextbox(master=self.tableFrame,height = 40,corner_radius=1,
                                                                 font=customtkinter.CTkFont(size=15),width=self.w[f-1])
                    self.PrintDetails.grid(row = j1, column = f, padx=5 , pady=5, sticky = "nsew")
                    self.PrintDetails.insert(END,k)
                    f=f+1
                    self.search_results.append(self.PrintDetails)
                    self.sallis.append(self.PrintDetails)
            
        else:
            messagebox.showerror('Not Found', f'Salary details of Empolyee with S.No. {sno} do not exist')
            return

        cur.close()


    
    def _ctsv(self,x):
        return StringVar(value=str(x))
    
    def des(self,l):
        for i in l:
            i.destroy()
        l.clear()



