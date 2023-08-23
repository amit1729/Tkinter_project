import customtkinter
from tkinter import *
from tkinter import messagebox
import datetime
from .utils import validAmount, validPercent, chageFormat, validNumber
from functools import partial

class UpdateSalary(customtkinter.CTkScrollableFrame):
    def __init__(self,master,connection, id = ''):
        super().__init__(master, label_text='Update Salary')
        self.master = master
        self.con = connection
        self.grid(row=0, column=1,rowspan=4, padx=(20, 0), pady=(20,0), sticky="nsew")
        self.grid_columnconfigure((1,2,4), weight = 1)
        self.grid_columnconfigure(3, weight = 2)
        # Dictionary with id as key and a tuple as value (label widget, button widget)
        self.startRow = 0
        self.idDict = {}

        

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
        self.height = 0
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

        self.nextButton = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text='Next', command=self.nextButtonClicked)
        

        self.clearButton = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text='Clear',command=self.clearButtonClicked)
        

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
        self.nextButton.grid(row=13, column=3, padx=(20, 20), pady=(20, 20), sticky="w")
        self.clearButton.grid(row=13, column=2, padx=(20, 20), pady=(20, 20), sticky="e")

        self.params = {
                'basic': ['Basic Pay', self.basicEntry, self.basicLabel,6],
                'da': ['DA(%)', self.daEntry,self.daLabel,7],
                'tpt': ['TPT', self.tptEntry, self.tptLabel,8],
                'hra': ['HRA(%)',self.hraEntry, self.hraLabel,9],
                'gmc': ['GMC(%)',self.gmcEntry,self.gmcLabel,10],
                'indvc': ['INDV Contri',self.indvcEntry,self.indvcLabel,11],
                'cgeis': ['CGEIS',self.cgeisEntry,self.cgeisLabel,12]
            }

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

            
            self.cbFrame = customtkinter.CTkFrame(self,fg_color='#333333')
            self.cbFrame.grid(row = 2, column = 2,columnspan = 2, pady=(20,0), sticky = '')
            for i,p in enumerate(self.params.keys()):
                cb = customtkinter.CTkCheckBox(self.cbFrame, text=self.params[p][0], onvalue=1, offvalue=0, checkbox_height=20, checkbox_width=20, command=partial(self.cbEvent,p))
                if i//4 == 0:
                    cb.grid(row = i//4, column = i%4, padx=(15, 15), pady=(10,10), sticky = 'w')
                else:
                    cb.grid(row = i//4, column = i%4, padx=(15, 15), pady=(0,10), sticky = 'w')
                self.params[p].append(cb)
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

    def fetchPersonalDetails(self,id):
        cur = self.con.cursor()
        res = cur.execute("SELECT * FROM Personal WHERE id = ?",
               (id,))
        row = res.fetchone()
        cur.close()
        flag = not row == None
        return row, flag
    
    def getResults(self):
        # Returns list of unique ids with string to display attached (id, string to display)
        # pass
        
        idRange = self.idEntry.get()
        idRange = idRange.split(':')
        if len(idRange) == 1: idRange.append(idRange[0])
        if not (validNumber(idRange[0]) and validNumber(idRange[1])):
            messagebox.showerror('Invalid Input', 'Invalid number or number range \nTo input number range use \':\'.\n Ex. 2:5 Range includes both 2 and 5')
            return []
        idRange = list(map(int, idRange))
        res = []
        for i in range(idRange[0], idRange[1]+1,1):
            if i in self.idDict.keys(): continue
            row, exists = self.fetchPersonalDetails(i)
            if exists:
                res.append((i,f'{i} : {row[1]}, {row[2]}'))
            else:
                # Log Error message
                continue
        self.idEntry.delete(0,END)
        # print(res)
        return res
    
    def recordsRBEvent(self):
        if self.recordsVar.get():
            self.infoFrame = customtkinter.CTkScrollableFrame(self, height=self.height)
            self.infoFrame.grid(row = 5, column = 2,columnspan = 2, padx=(20, 20), pady=(20,0), sticky = 'ew')
            self.idEntry = customtkinter.CTkEntry(self, placeholder_text="Serial Number of Employees To Update")
            self.idEntry.grid(row = 4, column = 2,columnspan =2, padx=(20, 20), pady=(20,0), sticky = "ew")
            self.idEntry.bind('<Return>', command=self.enterPressed)
        else:
            self.infoFrame.grid_forget()
            self.idEntry.destroy()

    def enterPressed(self,event):
        # print(1)
        rec = self.getResults()
        for r in rec:
            self.height = self.height+50
            self.infoFrame.configure(height = min(150,self.height))
            label = customtkinter.CTkLabel(self.infoFrame, text=r[1], font=customtkinter.CTkFont(size=14,weight='bold', family='arial'), corner_radius=6, fg_color="#333333", padx = 15)
            label.grid(row = self.startRow, column = 0, padx=(20,5), pady=(10,0), sticky = 'ew')
            button = customtkinter.CTkButton(self.infoFrame, text='X',fg_color="gray10", border_width=2, text_color='white', width=28, font=customtkinter.CTkFont(size=14,weight='bold', family='arial'), command=partial(self.deleteButtonClicked, r[0]))
            button.grid(row = self.startRow, column = 1, padx=(0, 20), pady=(10,0), sticky = 'w')
          
            self.idDict[r[0]] = (label, button)
            self.startRow+=1

    def deleteButtonClicked(self, i):
        self.height = max(0, self.height-50)
        self.idDict[i][0].destroy()
        self.idDict[i][1].destroy()
        del self.idDict[i]

    def getFields(self):
        fields = []
        if self.paramVar.get():
            for k in self.params.keys():
                if self.params[k][4].get():
                    fields.append(k)
        else:
            fields = self.params.keys()
            
        return fields

    def allSelected(self, fields):
        if len(fields) == 7: return True
        if 'basic' in fields and 'da' in fields and 'tpt' in fields and 'hra' in fields and 'cgeis' in fields:
            return True
        return False

    def check(self, id):
        cur = self.con.cursor()
        res = cur.execute("SELECT * FROM Salary WHERE id = ? and date = ?",
               (id, chageFormat(f'01/{self.monthVar.get().lower()}/{self.yearVar.get()}','%d/%B/%Y', '%Y-%m-%d')))
        rows = res.fetchall()
        cur.close()
        if len(rows) == 0:
            return False
        else: return True

    def anyExists(self, id):
        cur = self.con.cursor()
        res = cur.execute("SELECT * FROM Salary WHERE id = ?",
               (id, ))
        rows = res.fetchall()
        cur.close()
        if len(rows) == 0:
            return False
        else: return True

    def buildUpdateQuery(self, fields):
        query = 'UPDATE Salary SET '
        for i in range(len(fields)):
            if i==0: 
                query+= f'{fields[i]} = ?'
            else:
                query+= f', {fields[i]} = ?'
        query+= ' WHERE id = ? and date = ?'
        return query

    def getValues(self, fields):
        vals = []
        for f in fields:
            if f=='gmc':
                vals.append(self.gmcVar.get())
            elif f=='indvc':
                vals.append(self.indvcVar.get())
            else:
                vals.append(self.params[f][1].get())
        return vals
    
    def fetchAllIds(self):
        cur = self.con.cursor()
        res = cur.execute("SELECT id FROM Personal")
        row = res.fetchall()
        row = list(map(lambda x:x[0], row))
        cur.close()
        return row
    
    def dbp(self):
        cur = self.con.cursor()
        res = cur.execute("SELECT * FROM Salary")
        row = res.fetchall()
        print(row)
    
    def getLatestData(self, id):
        cur = self.con.cursor()
        res = cur.execute('SELECT id, date, basic, da, tpt, gmc, indvc, cgeis, hra FROM Salary WHERE id = ? ORDER BY ABS(julianday(date)-julianday(?)) LIMIT 1', 
                          (id, chageFormat(f'01/{self.monthVar.get().lower()}/{self.yearVar.get()}','%d/%B/%Y', '%Y-%m-%d')))
        res = res.fetchone()
        cur.close()
        return list(res)
    
    def validationError(self, wdgt, msg):
        # self.editButtonClicked()
        wdgt.focus()
        messagebox.showerror('Input Error',  msg)
    
    def validate(self):
        # print(self.basicPay.get())
        if not self.paramVar.get():
            if not validAmount(self.basicEntry.get()):
                self.validationError(self.basicEntry, 'Please enter basic pay correctly')
                return False
            elif not validAmount(self.daEntry.get()):
                self.validationError(self.daEntry, 'Please enter DA(%) correctly')
                return False
            elif not validAmount(self.tptEntry.get()):
                self.validationError(self.tptEntry, 'Please enter TPT correctly')
                return False
            elif not validAmount(self.hraEntry.get()):
                self.validationError(self.hraEntry, 'Please enter HRA(%) correctly')
                return False
            elif not validAmount(self.gmcEntry.get()):
                self.validationError(self.gmcEntry, 'Please enter GMC(%) correctly')
                return False
            elif not validAmount(self.indvcEntry.get()):
                self.validationError(self.indvcEntry, 'Please enter Individual Contribution(%) correctly')
                return False
        else:
            if self.params['basic'][4].get() and not validAmount(self.basicEntry.get()):
                self.validationError(self.basicEntry, 'Please enter basic pay correctly')
                return False
            elif self.params['da'][4].get() and not validAmount(self.daEntry.get()):
                self.validationError(self.daEntry, 'Please enter DA(%) correctly')
                return False
            elif self.params['tpt'][4].get() and not validAmount(self.tptEntry.get()):
                self.validationError(self.tptEntry, 'Please enter TPT correctly')
                return False
            elif self.params['hra'][4].get() and not validAmount(self.hraEntry.get()):
                self.validationError(self.hraEntry, 'Please enter HRA(%) correctly')
                return False
            elif self.params['gmc'][4].get() and not validAmount(self.gmcEntry.get()):
                self.validationError(self.gmcEntry, 'Please enter GMC(%) correctly')
                return False
            elif self.params['indvc'][4].get() and not validAmount(self.indvcEntry.get()):
                self.validationError(self.indvcEntry, 'Please enter Individual Contribution(%) correctly')
                return False
        return True
    
    def nextButtonClicked(self):
        self.dbp()
        if self.validate():
            self.nextButton.destroy()
            self.clearButton.destroy()
            self.basicEntry.configure(state = 'disabled')
            self.daEntry.configure(state = 'disabled')
            self.tptEntry.configure(state = 'disabled')
            self.gmcEntry.configure(state = 'disabled')
            self.indvcEntry.configure(state = 'disabled')
            self.hraEntry.configure(state = 'disabled')
            self.cgeisEntry.configure(state = 'disabled')
            self.monthOptionMenu.configure(state= 'disabled')
            self.yearOptionMenu.configure(state= 'disabled')
            self.submitButton = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text='Submit', command=self.submitButtonClicked)
            self.submitButton.grid(row=13, column=3, padx=(20, 20), pady=(20, 0), sticky="w")

            self.editButton = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text='Edit', command=self.editButtonClicked)
            self.editButton.grid(row=13, column=2, padx=(20, 20), pady=(20, 0), sticky="e")

            self.msgLabel = customtkinter.CTkLabel(self, text="*Please Confirm the Details!", font=customtkinter.CTkFont(size=10, weight="bold"), anchor ='w',text_color='red')
            self.msgLabel.grid(row = 14, column = 1,columnspan = 4, padx=(20, 20), pady=(0,0), sticky = "ew")

    def editButtonClicked(self):
        self.submitButton.destroy()
        self.editButton.destroy()
        self.basicEntry.configure(state = 'normal')
        self.daEntry.configure(state = 'normal')
        self.tptEntry.configure(state = 'normal')
        self.gmcEntry.configure(state = 'normal')
        self.indvcEntry.configure(state = 'normal')
        self.hraEntry.configure(state = 'normal')
        self.cgeisEntry.configure(state = 'normal')
        self.monthOptionMenu.configure(state= 'normal')
        self.yearOptionMenu.configure(state= 'normal')
        self.nextButton = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text='Next', command=self.nextButtonClicked)
        self.nextButton.grid(row=13, column=3, padx=(20, 20), pady=(20, 20), sticky="w")

        self.clearButton = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text='Clear',command=self.clearButtonClicked)
        self.clearButton.grid(row=13, column=2, padx=(20, 20), pady=(20, 20), sticky="e")
        self.msgLabel.destroy()

    def clearButtonClicked(self):
        # self.basicEntry.delete(0,'end')
        # self.daEntry.delete(0,'end')
        # self.tptEntry.delete(0,'end')
        # self.gmcEntry.delete(0,'end')
        # self.indvcEntry.delete(0,'end')
        # self.hraEntry.delete(0,'end')
        self.height = 0
        self.infoFrame.configure(height = self.height)
        for i in self.idDict.keys():
            self.idDict[i][0].destroy()
            self.idDict[i][1].destroy()
        self.idDict = {}
        self.startRow = 0


    def submitButtonClicked(self):
        fields = self.getFields()
        cur = self.con.cursor()
        if not self.recordsVar.get():
            ids = self.fetchAllIds()
        else:
            ids = self.idDict.keys()
        # print(ids)
        if len(fields)==0:
            messagebox.showerror('Invalid Parameters', 'Select Some fields to update')
            return
        if len(ids)==0:
            messagebox.showerror('No Records', 'No Records to Update')
        if self.allSelected(fields):
            fields = self.params.keys()
            
            for id in ids:
                if self.check(id):
                    cur.execute(self.buildUpdateQuery(fields), (*self.getValues(fields), id, chageFormat(f'01/{self.monthVar.get().lower()}/{self.yearVar.get()}','%d/%B/%Y', '%Y-%m-%d')))
                else:
                    cur.execute(
                        '''
                            INSERT INTO Salary (id, date, basic, da, tpt, hra, gmc, indvc, cgeis)
                            VALUES (?,?,?,?,?,?,?,?,?)
                        ''',
                        (id, chageFormat(f'01/{self.monthVar.get().lower()}/{self.yearVar.get()}','%d/%B/%Y', '%Y-%m-%d'),*self.getValues(fields))
                    )
        else:
            for id in ids:
                if self.anyExists(id):
                    if self.check(id):
                        cur.execute(self.buildUpdateQuery(fields), (*self.getValues(fields), id, chageFormat(f'01/{self.monthVar.get().lower()}/{self.yearVar.get()}','%d/%B/%Y', '%Y-%m-%d')))
                    else:
                        prev_vals = self.getLatestData(id)
                        prev_vals[1] = chageFormat(f'01/{self.monthVar.get().lower()}/{self.yearVar.get()}','%d/%B/%Y', '%Y-%m-%d')
                        if self.params['basic'][4].get(): prev_vals[2] = self.params['basic'][1].get()
                        if self.params['da'][4].get(): prev_vals[3] = self.params['da'][1].get()
                        if self.params['tpt'][4].get(): prev_vals[4] = self.params['tpt'][1].get()
                        if self.params['gmc'][4].get(): prev_vals[5] = self.gmcVar.get()
                        if self.params['indvc'][4].get(): prev_vals[6] = self.indvcVar.get()
                        if self.params['cgeis'][4].get(): prev_vals[7] = self.params['cgeis'][1].get()
                        if self.params['hra'][4].get(): prev_vals[8] = self.params['hra'][1].get()
                        cur.execute(
                        '''
                            INSERT INTO Salary (id, date, basic, da, tpt, hra, gmc, indvc, cgeis)
                            VALUES (?,?,?,?,?,?,?,?,?)
                        ''',
                        tuple(prev_vals)
                        )
                        # Log warnings here
                else:
                    messagebox.showerror('Invalid Parameters', 'Please Select ALL parameters')
                    return
        self.con.commit()
        cur.close()
        messagebox.showerror('Success', 'Records Updated successfully')
        self.editButtonClicked()




        

