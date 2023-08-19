import customtkinter
from tkinter import *
import datetime
from functools import partial
import sqlite3 as lite

class DisplaySheet(customtkinter.CTkScrollableFrame):
    def __init__(self,master,connection):
        super().__init__(master, label_text='Employee Details')
        self.con = connection
        cur = (self.con).cursor()
        self.grid(row=0, column=1,rowspan=4, padx=(20, 0), pady=(20,0), sticky="nsew")
        Employee_table=cur.execute("SELECT * FROM Personal")
        
        self.indexLabel = customtkinter.CTkLabel(self, text="Index", font=customtkinter.CTkFont(size=15, weight="bold"), anchor ='w')
        self.indexLabel.grid(row = 1, column = 1, padx=(20, 20), pady=(20,0), sticky = "ew")

        self.nameLabel = customtkinter.CTkLabel(self, text="Name", font=customtkinter.CTkFont(size=15, weight="bold"), anchor ='w')
        self.nameLabel.grid(row = 1, column = 2, padx=(20, 20), pady=(20,0), sticky = "ew")
        
        self.rankLabel = customtkinter.CTkLabel(self, text="Rank", font=customtkinter.CTkFont(size=15, weight="bold"),anchor = 'w')
        self.rankLabel.grid(row = 1, column = 3, padx=(20, 20), pady=(20,0), sticky = "ew")
        
        self.mobnoLabel = customtkinter.CTkLabel(self, text="Mobile Number", font=customtkinter.CTkFont(size=15, weight="bold"),anchor = 'w')
        self.mobnoLabel.grid(row = 1, column = 4, padx=(20, 20), pady=(20,0), sticky = "ew")
        
        self.dobLabel = customtkinter.CTkLabel(self, text="Date of Birth", font=customtkinter.CTkFont(size=15, weight="bold"),anchor = 'w')
        self.dobLabel.grid(row = 1, column = 5, padx=(20, 20), pady=(20,0), sticky = "ew")
        
        self.coLabel = customtkinter.CTkLabel(self, text="CO", font=customtkinter.CTkFont(size=15, weight="bold"),anchor = 'w')
        self.coLabel.grid(row = 1, column = 6, padx=(20, 20), pady=(20,0), sticky = "ew")

        j=1

        for i in Employee_table:
            j=j+1

            self.printind = customtkinter.CTkLabel(self, text=i[0], font=customtkinter.CTkFont(size=15, weight="bold"), anchor ='w')
            self.printind.grid(row = j, column = 1, padx=(20, 20), pady=(20,0), sticky = "ew")

            self.printname = customtkinter.CTkLabel(self, text=i[1], font=customtkinter.CTkFont(size=15, weight="bold"), anchor ='w')
            self.printname.grid(row = j, column = 2, padx=(20, 20), pady=(20,0), sticky = "ew")

            self.printrank = customtkinter.CTkLabel(self, text=i[4], font=customtkinter.CTkFont(size=15, weight="bold"), anchor ='w')
            self.printrank.grid(row = j, column = 3, padx=(20, 20), pady=(20,0), sticky = "ew")

            self.printmno = customtkinter.CTkLabel(self, text=i[5], font=customtkinter.CTkFont(size=15, weight="bold"), anchor ='w')
            self.printmno.grid(row = j, column = 4, padx=(20, 20), pady=(20,0), sticky = "ew")

            self.printdob = customtkinter.CTkLabel(self, text=i[2], font=customtkinter.CTkFont(size=15, weight="bold"), anchor ='w')
            self.printdob.grid(row = j, column = 5, padx=(20, 20), pady=(20,0), sticky = "ew")

            self.printco = customtkinter.CTkLabel(self, text=i[3], font=customtkinter.CTkFont(size=15, weight="bold"), anchor ='w')
            self.printco.grid(row = j, column = 6, padx=(20, 20), pady=(20,0), sticky = "ew")


        cur.close()

