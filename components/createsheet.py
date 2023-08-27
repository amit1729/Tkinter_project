import customtkinter
from tkinter import *
import datetime
from functools import partial
from .utils import chageFormat, validNumber
from tkinter import messagebox, filedialog
import xlsxwriter
import calendar
import os
from .utils import validAmount, validPercent, chageFormat, log_errors_to_file, runtimelog
# from .tableframe import CustomTable
@log_errors_to_file('out/errorlogs.txt')
class CreateSheet(customtkinter.CTkScrollableFrame):
    
    def __init__(self,master,connection):
        super().__init__(master, label_text='Create Monthly Salary Report')
        self.con = connection
        self.grid(row=0, column=1,rowspan=4, padx=(20, 0), pady=(20,0), sticky="nsew")
        
        # self.grid_columnconfigure((1,4,6,8,10,13), weight = 2)
        # self.grid_columnconfigure(2, weight = 1)
        # self.grid_columnconfigure((3,5,7,9,11,12), weight = 3)
        x = 7
        y = 4
        z = 1

        self.flag=0
        
        self.idDict={}
        self.array_search_emp=[]
        self.serial_no=0

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

       
        self.basicPay = self._ctsv('200000')
        self.da = self._ctsv('20')
        self.tda = self._ctsv('20000')
        self.daontda = self._ctsv('20')
        self.deductions = self._ctsv('2000')
        self.hra = self._ctsv('10')
        
        self.entries = {}
        self.entryIds = {}
        self.index = 0

        today = datetime.date.today()

        self.dateLabel = customtkinter.CTkLabel(self, text="Create the pay sheet for the month of: ", font=customtkinter.CTkFont(size=17, weight="bold"),anchor = 'w')
        self.dateLabel.grid(row = 0, column = 1 , columnspan = 7, padx=(20, 20), pady=(20,0), sticky = "ew")

        self.monthList = ['January', 'February', 'March', 'April','May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        self.monthVar = StringVar(value=self.monthList[today.month-1])
        self.monthOptionMenu = customtkinter.CTkOptionMenu(self,values=self.monthList,variable=self.monthVar)
        self.monthOptionMenu.grid(row = 0, column = 8 , columnspan = 3, padx=(30, 20), pady=(20,0), sticky = "w")

        self.yearList = list(map(str, list(range(today.year-15,today.year+2,1))))
        self.yearVar = StringVar(value=str(today.year))
        self.yearOptionMenu = customtkinter.CTkOptionMenu(self,values=self.yearList,variable=self.yearVar)
        self.yearOptionMenu.grid(row = 0, column = 11 , columnspan = 3, padx=(20, 30), pady=(20,0), sticky = "e")

        self.snoEntry = customtkinter.CTkEntry(self, placeholder_text="Serial Number of Employee")
        self.snoEntry.grid(row = 1, column = 1 , columnspan = 7, padx=(20, 20), pady=(20,0), sticky = "ew")
        self.searchButton = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text='Search Employee', command=self.searchButtonClicked)
        self.searchButton.grid(row=1, column=8, columnspan = 6, padx=(20, 20), pady=(20, 0), sticky="ew")
        self.snoEntry.bind('<Return>', command=self.enterPressed)
        self.textbox = customtkinter.CTkTextbox(master=self,height = 100, width = 150)
        self.textbox.grid(row=2, column=1, columnspan = 7,padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.searchButton = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"),hover_color='green', text='Add',height = 80, command=self.addButtonClicked)
        # self.searchButton.configure(state = 'hidden')
        self.searchButton.grid(row=2, column=8, columnspan = 3, padx=(20, 20), pady=(20, 20), sticky="ew")
        
        self.exportButton = customtkinter.CTkButton(master=self, border_width=2, text_color=("gray10", "#DCE4EE"), text='Export',height = 80, command=self.exportButtonClicked)
        self.exportButton.grid(row=2, column=11, columnspan = 3, padx=(20, 20), pady=(20, 20), sticky="ew")
        # self.exportButton.configure(state = 'hidden')
        # self.tableFrame = CustomTable(self,self.con)
    @log_errors_to_file('out/errorlogs.txt')
    def enterPressed(self,event):
        self.searchButtonClicked()

    @log_errors_to_file('out/errorlogs.txt')
    def _ctsv(self,x):
        return StringVar(value=str(x))
    
    @log_errors_to_file('out/errorlogs.txt')
    def fetchPersonalDetail(self,i):
        cur = self.con.cursor()
        res = cur.execute("SELECT * FROM Personal WHERE id = ?",
               (i,))
        row = res.fetchone()
        cur.close()
        flag = not row == None
        return row, flag
    
    @log_errors_to_file('out/errorlogs.txt')
    def getResults(self):
        # Returns list of unique ids with string to display attached (id, string to display)
        # pass
        
        idRange = self.snoEntry.get()
        idRange = idRange.split(':')
        if len(idRange) == 1: idRange.append(idRange[0])
        if not (validNumber(idRange[0]) and validNumber(idRange[1])):
            messagebox.showerror('Invalid Input', 'Invalid number or number range \nTo input number range use \':\'.\n Ex. 2:5 Range includes both 2 and 5')
            return []
        idRange = list(map(int, idRange))
        res = []
        already_present=""
        wrong_ent=""
        for i in range(idRange[0], idRange[1]+1,1):
            if i in self.idDict.keys():
                already_present=already_present+' '+str(i) 
                continue
            row, exists = self.fetchPersonalDetail(i)
            if exists:
                res.append((f'{row[1]}', f'{i}', f'{row[7]}'))
            else:
                wrong_ent=wrong_ent+" "+str(i)
                continue
        if(len(already_present)>0 and self.flag==0):
            messagebox.showerror('Duplicate', f'Salary record for Empolyee with serial numbers{already_present} for the month of {self.monthOptionMenu.get()} {self.yearOptionMenu.get()} already exists')
        if(len(wrong_ent)>0 and self.flag==0):
            messagebox.showerror('Not Found', f'Salary record for Empolyee with serial numbers {wrong_ent} for the month of {self.monthOptionMenu.get()} {self.yearOptionMenu.get()} does not exists')
        return res

    '''
    
    def searchButtonClicked(self):
        data, exists = self.fetchPersonalDetails()
        if exists:
            self.name = self._ctsv(data[1])
            self.id = self._ctsv(data[0])
            self.pran = self._ctsv(data[7])
            self.rank= self._ctsv(data[2])
            self.citycode=self._ctsv(data[4])
            self.doj=self._ctsv(data[5])
            self.doi=self._ctsv(data[6])
            # self.textbox = customtkinter.CTkTextbox(master=self,height = 100, width = 150)
            # self.textbox.grid(row=2, column=1, columnspan = 7,padx=(20, 20), pady=(20, 20), sticky="nsew")
            self.textbox.configure(state = 'normal')
            self.textbox.delete('0.0', END)
            self.textbox.insert('0.0', f'Name - {self.name.get()}\nPer No. - {self.id.get()}\nPRAN - {self.pran.get()}')
            self.textbox.configure(state = 'disabled')
            # self.searchButton.configure(state = 'normal')
            # self.exportButton.configure(state = 'normal')
            # self.searchButton = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"),hover_color='green', text='Add',height = 80, command=self.addButtonClicked)
            # self.searchButton.grid(row=2, column=8, columnspan = 3, padx=(20, 20), pady=(20, 20), sticky="ew")
            # self.exportButton = customtkinter.CTkButton(master=self, border_width=2, text_color=("gray10", "#DCE4EE"), text='Export',height = 80, command=self.exportButtonClicked)
            # self.exportButton.grid(row=2, column=11, columnspan = 3, padx=(20, 20), pady=(20, 20), sticky="ew")
        else:
            messagebox.showerror('Not Found', f'Empolyee with serial number {self.snoEntry.get()} does not exists')
        '''

    @log_errors_to_file('out/errorlogs.txt')
    def searchButtonClicked(self):
        res = self.getResults()
        i=0
        for wid in self.array_search_emp:
            zz=f"{3*i+2}.0"
            if(i==0):
                zz="0.0"
            wid.configure(state = 'normal')
            wid.delete(zz,END)
            wid.configure(state = 'disabled')
            i=i+1
        self.array_search_emp=[]
        i=0
        for data in res:
            #self.rank= self._ctsv(data[2])
            #self.citycode=self._ctsv(data[4])
            #self.doj=self._ctsv(data[5])
            #self.doi=self._ctsv(data[6])
            # self.textbox = customtkinter.CTkTextbox(master=self,height = 100, width = 150)
            # self.textbox.grid(row=2, column=1, columnspan = 7,padx=(20, 20), pady=(20, 20), sticky="nsew")
            self.textbox.configure(state = 'normal')
            zz=f"{4*i+1}.0"
            if(i==len(res)-1):
                self.textbox.insert(zz, f'Name - {data[0]}\nPer No. - {data[1]}\nPRAN - {data[2]}')
            else:
                self.textbox.insert(zz, f'Name - {data[0]}\nPer No. - {data[1]}\nPRAN - {data[2]}\n\n')
            self.textbox.configure(state = 'disabled')
            self.array_search_emp.append(self.textbox)
            i=i+1
            # self.searchButton.configure(state = 'normal')
            # self.exportButton.configure(state = 'normal')
            # self.searchButton = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"),hover_color='green', text='Add',height = 80, command=self.addButtonClicked)
            # self.searchButton.grid(row=2, column=8, columnspan = 3, padx=(20, 20), pady=(20, 20), sticky="ew")
            # self.exportButton = customtkinter.CTkButton(master=self, border_width=2, text_color=("gray10", "#DCE4EE"), text='Export',height = 80, command=self.exportButtonClicked)
            # self.exportButton.grid(row=2, column=11, columnspan = 3, padx=(20, 20), pady=(20, 20), sticky="ew")

    @log_errors_to_file('out/errorlogs.txt')
    def disable(self, widgt):
        widgt.configure(state = 'disable')

    @log_errors_to_file('out/errorlogs.txt')
    def check(self, id):
        cur = self.con.cursor()
        res = cur.execute("SELECT * FROM Salary WHERE id = ? and date = ?",
               (id, chageFormat(f'01/{self.monthVar.get().lower()}/{self.yearVar.get()}','%d/%B/%Y', '%Y-%m-%d')))
        rows = res.fetchone()
        cur.close()
        if not rows:
            return None
        else: return rows
    
    @log_errors_to_file('out/errorlogs.txt')
    def getLatestData(self, id):
        cur = self.con.cursor()
        res = cur.execute('SELECT id, date, basic, da, tpt, gmc, indvc, cgeis, hra FROM Salary WHERE id = ? ORDER BY ABS(julianday(date)-julianday(?)) LIMIT 1', 
                          (id, chageFormat(f'01/{self.monthVar.get().lower()}/{self.yearVar.get()}','%d/%B/%Y', '%Y-%m-%d')))
        res = res.fetchone()
        cur.close()
        if not res:
            return None
        else: return res

    @log_errors_to_file('out/errorlogs.txt')
    def fetchSal(self,ind):
        row = self.check(ind)
        row2 = self.getLatestData(ind)
        if row:
            return row, True
        elif row2:
            # Print log that using closest date data
            runtimelog(ind)
            return row2, True
        else:
            return None, False

        # month_num={
        #         "JANUARY": "01",
        #         "FEBRUARY": "02",
        #         "MARCH": "03",
        #         "APRIL": "04",
        #         "MAY": "05",
        #         "JUNE": "06",
        #         "JULY": "07",
        #         "AUGUST": "08",
        #         "SEPTEMBER": "09",
        #         "OCTOBER": "10",
        #         "NOVEMBER": "11",
        #         "DECEMBER": "12"
        #     }
        # cur = self.con.cursor()
        
        # res = cur.execute("SELECT * FROM Salary WHERE id = ? AND strftime('%m', date) = ? AND strftime('%Y', date) = ?",
        #        (ind,month_num.get(self.monthOptionMenu.get().upper()),self.yearOptionMenu.get()))

        # row = res.fetchall()
        
        # cur.close()
        # if len(row) > 1:
        #     messagebox.showwarning('Multiple Entries', f'Multiple Entries Found')
        # flag = not len(row) == 0
        # if flag: return row[0], flag
        # else: return None,flag
    @log_errors_to_file('out/errorlogs.txt')
    def calPercent(self,base, percent):
        return round(float(base)*float(percent)/100,2)

    @log_errors_to_file('out/errorlogs.txt')
    def createRecord(self):

        idRange = self.snoEntry.get()
        idRange = idRange.split(':')
        if len(idRange) == 1: idRange.append(idRange[0])
        if not (validNumber(idRange[0]) and validNumber(idRange[1])):
            messagebox.showerror('Invalid Input', 'Invalid number or number range \nTo input number range use \':\'.\n Ex. 2:5 Range includes both 2 and 5')
            return []
        idRange = list(map(int, idRange))
        record=[]
        wrong_ent=""
        already_exist=""
        for ind in range(idRange[0],idRange[1]+1,1):
            if(ind not in self.entryIds.keys()):
                salData, salExists = self.fetchSal(ind)
                per_data, perExists=self.fetchPersonalDetail(ind)
                if salExists:
                    self.serial_no=self.serial_no+1
                    self.entryIds[ind]=salData[0]
                    basicPay = salData[2]
                    da = salData[3]
                    tpt = salData[4]
                    hra = salData[8]
                    gmc= salData[5]
                    indvc= salData[6]
                    cgeis= salData[7]

                    month=int(salData[1][5:7])
                    year=int(salData[1][0:4])
                    num_days=calendar.monthrange(year, month)[1]
                    self.hpld=num_days
                    hpla=round(((basicPay+da)*0)/self.hpld)
                    self.eold=num_days
                    eola=round(((basicPay+da)*0)/self.eold)
                    daontpt=round((da*tpt)/100.0)
                    gmconbpda=round((gmc*(basicPay+da))/100.0)
                    indlc=round((indvc*(basicPay+da))/100.0)
                    grossenwithoutgmc=basicPay+da+tpt+hra       # 3,5,6,8
                    grossen=basicPay+da+tpt+hra+gmconbpda       # 3,5,6,8,12
                    totded=cgeis+gmconbpda+indlc+hpla+eola      # 12,15,17,22,24
                    amtpay=grossen-totded                       # 13,25


                    record.append([
                            self.serial_no, #0
                            f'{per_data[1]}\nPer No. - {per_data[0]}\nPRAN - {per_data[7]}',
                            f'{per_data[2]}\n{per_data[4]}\n{per_data[5]}\n{per_data[6]}',
                            basicPay, #3
                            da, #4
                            round(self.calPercent(basicPay,da)), #5
                            tpt, #6
                            daontpt, #7         
                            round(self.calPercent(basicPay,hra)), #8
                            0,                #wa 9
                            0,                #Extra claim 10
                            grossenwithoutgmc,            #11
                            gmconbpda, #12
                            grossen,      #13          
                            gmconbpda,       #14  
                            indlc,             #15
                            0,                #cghs 16
                            round(cgeis), #17
                            0,                #licence 18
                            0,                #other deduction 19
                            0,                #income tax  20
                            0, #21
                            hpla, #22
                            0, #23
                            eola, #24
                            totded,  #25         
                            amtpay,     #26        
                            ])
                else:
                    wrong_ent=wrong_ent+" "+str(ind)
            else:
                already_exist=already_exist+" "+str(ind)
        
        if(len(wrong_ent)>0):
            messagebox.showerror('Not Found', f'Salary record for Empolyee with serial numbers{wrong_ent} for the month of {self.monthOptionMenu.get()} {self.yearOptionMenu.get()} does not exists')
        if(len(already_exist)>0):
            messagebox.showerror('Duplicate', f'Salary record for Empolyee with serial numbers{already_exist} for the month of {self.monthOptionMenu.get()} {self.yearOptionMenu.get()} already exists')
        return record, True
    
    @log_errors_to_file('out/errorlogs.txt')
    def buildHeader(self):
        self.headers = [
            ("S. No.", 0, 0, 4, 1),
            ('PERSONAL NUMBER\n AND DETAILS OF GOVT SERVANT', 0,1,4,1),
            ('RANK\n STATION\n DOJ\n DOI',0,2,4,1),
            ('ALLOWANCES', 0,3,1,11),
            ('RECOVERY', 0, 14, 1, 13),
            ('', 0,25,1,1),
            ('BP', 1,3,3,1),
            ('DEARNESS\nALLOWANCES',1,4,1,2),
            ('DA%',2,4,2,1),
            ('DA',2,5,2,1),
            ('TRANSPORT\nALLOWANCE',1,6,1,2),
            ('TPT',2,6,2,1),
            ('DA ON\nTPT',2,7,2,1),
            ('HRA',1,8,3,1),
            ('WASHING\nALLOWANCE',1,9,3,1),
            ('EXTRA\nCLAIM\n(SMALL\nFAMILY\nNORMS)',1,10,3,1),
            ('GROSS\nENTITLEME\nNT (EXCEPT\nGMC)',1,11,3,1),
            ('GMC% OF\n(BP+DA)',1,12,3,1),
            ('GROSS\nENTITLEMENT',1,13,3,1),
            ('GMC% OF\n(BP+DA)',1,14,3,1),
            ('INDL\nCONTRI% OF\n(BP+DA)',1,15,3,1),
            ('CGHS',1,16,3,1),
            ('CGEIS',1,17,3,1),
            ('LICENCE\nFEE MES\nBILLS',1,18,3,1),
            ('OTHER\nDEDUCTION/\nFESTIVAL\nADVANCE',1,19,3,1),
            ('INCOME\nTAX\n(PAID)',1,20,3,1),
            ('ABSENTY/HPL/EOL DEDUCTIONS',1,21,1,4),
            ('HPL',2,21,1,2),
            ('EOL',2,23,1,2),
            ('DAYS',3,21,1,1),
            ('AMT',3,22,1,1),
            ('DAYS',3,23,1,1),
            ('AMT',3,24,1,1),
            ('TOTAL\nDEDN',1,25,3,1),
            ('AMOUNT\nPAYABLE',1,26,3,1),
            ('ACTION',0,27,4,1)
        ]
        self.height = 150
        self.tableFrame = customtkinter.CTkScrollableFrame(self,corner_radius=0,orientation='horizontal')
        self.tableFrame.grid(row=3, column=1,columnspan = 13, pady=(20,0), sticky="nsew")
        # self.tableFrame.grid_rowconfigure((0,2,3),weight=1)
        self.tableFrame.grid_rowconfigure(1,weight=5)
        self.tableFrame.grid_rowconfigure(0,weight=1)
        self.tableFrame.grid_rowconfigure(2,weight=1)
        self.tableFrame.grid_rowconfigure(3,weight=1)
        self.tableFrame.grid_columnconfigure((0,),weight=1)
        for header in self.headers:
            self.ele=customtkinter.CTkLabel(master=self.tableFrame,text=header[0], corner_radius=2,font=customtkinter.CTkFont(size=12, weight='bold'),bg_color='#2b2b2b',padx  = 15)
            self.ele.grid(row=header[1], column=header[2],rowspan = header[3], columnspan = header[4] ,padx=(1,1), pady=(1,1),sticky="nsew")
            # self.ele.insert(END, header[0],"center")

    @log_errors_to_file('out/errorlogs.txt')
    def addButtonClicked(self):
        if self.snoEntry.get() == '':
            messagebox.showerror('Not Found',"No entry found")
            return
        
        self.flag=1
        self.searchButtonClicked()
        self.flag=1
        records, exists = self.createRecord()
        
        if exists:
            
            if self.index == 0 and len(records)>0:
                self.buildHeader()
                # self.height = 30
                # self.tableFrame = customtkinter.CTkScrollableFrame(self,corner_radius=0,orientation='horizontal')
                # self.tableFrame.grid(row=3, column=1,columnspan = 13, pady=(20,0), sticky="nsew")
                # for i, header in enumerate(self.headers):
                #     self.ele = customtkinter.CTkEntry(self.tableFrame,corner_radius=0,font=customtkinter.CTkFont(size=11))
                #     self.ele.grid(row = self.index+3, column = i+1, sticky = 'snew')
                #     self.ele.insert(END, header)
                #     self.disable(self.ele)

            for record in records:
                self.height+=70
                self.tableFrame.configure(height = self.height)
                elements = []
                ind=int(record[1].split('\n')[1].split(" ")[3])

                for i, rec in enumerate(record):
                    if i == 1 or i==2:
                        self.ele = customtkinter.CTkTextbox(master=self.tableFrame,height = 70,corner_radius=0,font=customtkinter.CTkFont(size=12))
                        self.ele.grid(row=self.index+4, column=i, sticky="nsew")
                        self.ele.insert(END,rec)
                        self.disable(self.ele)
                        elements.append(self.ele)
                    elif i in [9,10,16,18,19,20,21,23]:
                        self.ele = customtkinter.CTkEntry(master=self.tableFrame,placeholder_text="0",corner_radius=0,font=customtkinter.CTkFont(size=12))
                        self.ele.grid(row=self.index+4, column=i, sticky="nsew")
                        if(not(rec=="")):
                            self.ele.insert(END,rec)
                        self.ele.configure(state=NORMAL)
                        self.ele.bind('<Return>', command=partial(self.updateButtonClicked, ind))
                        self.ele.bind('<FocusOut>', partial(self.updateButtonClicked, ind))
                        elements.append(self.ele)
                    else:
                        self.ele = customtkinter.CTkEntry(master=self.tableFrame,placeholder_text="0",corner_radius=0,font=customtkinter.CTkFont(size=12))
                        self.ele.grid(row=self.index+4, column=i, sticky="nsew")
                        if(not(rec=="")):
                            self.ele.insert(END,rec)
                        self.ele.configure(state=NORMAL)
                        self.disable(self.ele)
                        elements.append(self.ele)
                
                self.deleteButton = customtkinter.CTkButton(master=self.tableFrame, fg_color="transparent", border_width=2,hover_color='red', text_color=("gray10", "#DCE4EE"), text='Remove', command=partial(self.deleteButtonClicked, ind),font=customtkinter.CTkFont(size=12, weight='bold'))
                self.deleteButton.grid(row=self.index+4, column=i+1, padx=(5, 5),pady = (5,5), sticky="nsew")
                elements.append(self.deleteButton)
                self.entries[ind] = [elements, record]
                self.entryIds[ind] = record
                self.index+=1

        self.snoEntry.delete(0,END)

    @log_errors_to_file('out/errorlogs.txt')
    def evaluateRow(self, i):
        entries = self.entries[i][0]
        vals = [0,0,0]
        for j in range(3,27):
            # print(j)
            vals.append(float(entries[j].get()))
        for j in range(len(vals)):
            if vals[j] == '':
                vals[j] = 0
        vals[11] = vals[3] + vals[5] + vals[7] + vals[8]+vals[9]+vals[10]
        vals[13] = vals[11] + vals[12]
        vals[22] = ((vals[3]+vals[5])*vals[21])/(2*self.eold)
        vals[24] = ((vals[3]+vals[5])*vals[23])/(self.eold)
        vals[25] = vals[14]+vals[15]+vals[16]+vals[17]+vals[18]+vals[19]+vals[20]+vals[22]+vals[24]
        vals[26] = vals[13]-vals[25]
        for j in range(3,27):
            self.entries[i][0][j].configure(state=NORMAL)
            self.entries[i][0][j].delete(0,END)
            self.entries[i][0][j].insert(END,round(vals[j]))
            if j not in [9,10,16,18,19,20,21,23]:
                self.disable(self.entries[i][0][j])
            self.entries[i][1][j] = vals[j]
            
    @log_errors_to_file('out/errorlogs.txt')
    def updateButtonClicked(self,i,event):
        self.evaluateRow(i)
        # old_data=[0,0,0,0,0,0,0,0]
        # old_data_ind=0
        # for j in [9,10,16,18,19,20,21,23]:
        #     k1=self.entries[i][0][j].get()
        #     if((j==21 or j==23) and (not k1=="")):
        #         if(int(k1)>self.hpld):
        #             self.entries[i][0][j].delete(0,END)
        #             self.entries[i][0][j].insert(END,self.entries[i][1][j])
        #             messagebox.showerror('Error', 'Number of days are greater than total days in month')
        #             return
        #     if(not (self.entries[i][1][j] ==  "" )):
        #         old_data[old_data_ind]=self.entries[i][1][j]
        #     if(j in [21,23]):
        #         old_data[old_data_ind]=self.entries[i][1][j+1]
        #     if(self.entries[i][0][j].get()!=""):
        #         k1=float(k1)
        #         self.entries[i][1][j]=k1
        #     if(self.entries[i][1][j]==""):
        #         self.entries[i][1][j]=float(0.0)
        #     old_data_ind=old_data_ind+1
        # self.entries[i][1][22]=round(((self.entries[i][1][3]+self.entries[i][1][5])*self.entries[i][1][21])/(2*self.eold),0)
        # self.entries[i][1][24]=round(((self.entries[i][1][3]+self.entries[i][1][5])*self.entries[i][1][23])/self.eold,0)
        # self.entries[i][1][11]=self.entries[i][1][3]+self.entries[i][1][5]+self.entries[i][1][6]+self.entries[i][1][8]+self.entries[i][1][9]+self.entries[i][1][10]-old_data[0]-old_data[1]
        # self.entries[i][1][13]=self.entries[i][1][3]+self.entries[i][1][5]+self.entries[i][1][6]+self.entries[i][1][8]+self.entries[i][1][12]+self.entries[i][1][9]+self.entries[i][1][10]-old_data[0]-old_data[1]
        # self.entries[i][1][25]=self.entries[i][1][12]+self.entries[i][1][15]+self.entries[i][1][17]+self.entries[i][1][22]+self.entries[i][1][24]+self.entries[i][1][16]+self.entries[i][1][18]+self.entries[i][1][19]+self.entries[i][1][20]+self.entries[i][1][22]+self.entries[i][1][24]-old_data[2]-old_data[3]-old_data[4]-old_data[5]-old_data[6]-old_data[7]
        # self.entries[i][1][26]=self.entries[i][1][13]-self.entries[i][1][25]

        # for j in [11,13,22,24,25,26]:
        #     self.entries[i][0][j].configure(state=NORMAL)
        #     self.entries[i][0][j].delete(0,END)
        #     self.entries[i][0][j].insert(END,self.entries[i][1][j])
        #     self.disable(self.entries[i][0][j])

    @log_errors_to_file('out/errorlogs.txt')
    def deleteButtonClicked(self, i):
        del_sno=self.entries[i][0][0].get()
        for ele in self.entries.values():
            if ele[0][0].get() > del_sno:
                ele[1][0]=ele[1][0]-1
                ele[0][0].configure(state=NORMAL)
                ele[0][0].delete(0,END)
                ele[0][0].insert(END,ele[1][0])
                ele[0][0].configure(state=DISABLED)

        self.serial_no=self.serial_no-1

        for ele in self.entries[i][0]:
            ele.destroy()
        del self.entries[i]
        del self.entryIds[i]
        self.height-=70
        self.tableFrame.configure(height = self.height)
        if len(self.entries)==0:
            self.tableFrame.destroy()
            self.index = 0

    @log_errors_to_file('out/errorlogs.txt')
    def exportButtonClicked(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Workbook", "*.xlsx"), ],
            title="Save As"
            )
        if file_path:
            workbook = xlsxwriter.Workbook(file_path)
            worksheet = workbook.add_worksheet()
            printable_area = 14*72

            color_format1 = workbook.add_format({'bg_color': '#efb5da', 'bold': True, 'text_wrap': True, 'align': 'center', 'valign': 'vcenter','font_size': 18,'font_name': 'cambria','align': 'center', 'valign': 'vcenter'})
            color_format8 = workbook.add_format({'bg_color': '#b2d366', 'bold': True, 'text_wrap': True, 'align': 'center', 'valign': 'vcenter','font_size': 11,'font_name': 'calibri','align': 'left', 'valign': 'vcenter'})
            color_format9 = workbook.add_format({'bg_color': '#efb5da', 'bold': True, 'text_wrap': True, 'align': 'center', 'valign': 'vcenter','font_size': 11,'font_name': 'calibri','align': 'left', 'valign': 'vcenter'})
            color_format10 = workbook.add_format({'bg_color': '#efb5da', 'bold': True, 'text_wrap': True, 'align': 'center', 'valign': 'vcenter','font_size': 11,'font_name': 'calibri','align': 'center', 'valign': 'vcenter'})
            
            color_format2 = workbook.add_format({'bg_color': '#a8a8a8','border': 1, 'border_color': 'black', 'bold': True, 'text_wrap': True, 'font_size': 8,'font_name': 'calibri', 'align': 'center', 'valign': 'vcenter'})
            color_format3 = workbook.add_format({'bg_color': '#fcfc7e','border': 1, 'border_color': 'black', 'bold': False, 'text_wrap': True, 'font_size': 8,'font_name': 'calibri', 'text_wrap': True,  'valign': 'vcenter','align': 'center'})
            color_format4=workbook.add_format({'bg_color': '#b2d366','border': 1, 'border_color': 'black', 'bold': False, 'text_wrap': True, 'font_size': 8,'font_name': 'calibri', 'text_wrap': True,  'valign': 'vcenter','align': 'center'})
            color_format14=workbook.add_format({'bg_color': '#b2d366', 'border_color': 'black', 'bold': False, 'text_wrap': True, 'font_size': 16,'font_name': 'cambria', 'text_wrap': True,  'valign': 'vcenter','align': 'center'})

            color_format5=workbook.add_format({'bg_color': '#a8a8a8','border': 1, 'border_color': 'black', 'bold': False, 'text_wrap': True, 'font_size': 8,'font_name': 'calibri', 'text_wrap': True,  'valign': 'vcenter','align': 'center'})
            color_format6=workbook.add_format({'bg_color': '#a8a8a8','border': 1, 'border_color': 'black', 'bold': True, 'text_wrap': True, 'font_size': 8,'font_name': 'calibri', 'text_wrap': True,  'valign': 'vcenter','align': 'center'})
            color_format7=workbook.add_format({'bg_color': '#efb5da'})

            color_format44=workbook.add_format({'bg_color': '#b2d366', 'border_color': 'black', 'bold': False, 'text_wrap': True, 'font_size': 14,'font_name': 'cambria', 'text_wrap': True,  'valign': 'vcenter','align': 'center'})
            worksheet.merge_range('A1:AA1', "REGULAR PAY BILL : DEFENCE CIVILIAN EMPLOYEES OF SWCCSR",color_format1)
            worksheet.merge_range('B2:D2', 'REGULAR PAY BILL FOR THE MONTH OF',color_format9)
            worksheet.merge_range('B3:D3', 'REGULAR PAY BILL NUMBER',color_format9)
            worksheet.write('S2:S2', 'UNIT',color_format9)
            worksheet.write('S3:S3', 'DATED',color_format9)
            worksheet.write('E2',':',color_format10)
            worksheet.write('E3',':',color_format10)
            worksheet.write('T2',':',color_format10)
            worksheet.write('T3',':',color_format10)
            worksheet.merge_range('F2:H2', f'{self.monthVar.get().upper()} {self.yearVar.get()}',color_format8)
            worksheet.merge_range('F3:H3', '',color_format8)
            worksheet.merge_range('U2:W2', '',color_format8)
            worksheet.merge_range('U3:W3', datetime.datetime.today().strftime('%d %B %Y'),color_format8)
            worksheet.merge_range('A2:A3', '', color_format7)
            worksheet.merge_range('I2:R3', '', color_format7)
            worksheet.merge_range('X2:AA3', '', color_format7)
            worksheet.merge_range('A4:AA4', '', color_format7)
            # rich_text = [color_format1,"REGULAR PAY BILL : DEFENCE CIVILIAN EMPLOYEES OF SWCCSR\n ",color_format8,"(NEW PENSION SCHEME)"]
            # worksheet.write_rich_string('A1', *rich_text)
            # worksheet.merge_range('C1:I1'," ",color_format7)
            # worksheet.merge_range('C4:I4'," ",color_format7)
            # worksheet.merge_range('J1:AA4'," ",color_format7)
            # worksheet.merge_range('C2:I3', f'Salary Report for the month of {self.monthOptionMenu.get()} {self.yearOptionMenu.get()}' ,color_format1)
            worksheet.set_column('B:B', 15)

            colns=self.columns_name(len(self.headers))

            for c in range(len(self.headers)):
                if(c==(len(self.headers)-1)):   continue
                if colns[c]!='B':
                    # worksheet.set_column(f'{colns[c]}:{colns[c]}', 10)
                    pass

                start_row=self.headers[c][1]
                start_col=self.headers[c][2]
                end_row=self.headers[c][3]
                end_col=self.headers[c][4]
                starting=colns[start_col]+str(start_row+5)
                ending=colns[start_col+end_col-1]+str(start_row+end_row+4)

                if(starting==ending):
                    worksheet.write(starting, self.headers[c][0],color_format2)
                else:
                    worksheet.merge_range(f'{starting}:{ending}', self.headers[c][0],color_format2 )

            
            
            records = list(map(lambda x: x[1], self.entries.values()))
            records.sort(key = lambda x: x[0])
            height = 200
            i = 0
            page_totals = []
            page_total = [0]*27
            for record in records:
                worksheet.set_row(i+8, 50)
                if (height + 100) <= printable_area:
                    colns=self.columns_name(len(self.headers))
                    for c in range(len(record)):
                        if(record[c]==""):
                            record[c]=round(float(0.0))
                        if c == 1 or c==2:
                            worksheet.write(colns[c]+str(i+9), record[c],color_format3)
                        elif c==0:
                            worksheet.write(colns[c]+str(i+9), int(record[c]),color_format3)
                        elif(c in [9,10,17,18,19,20]):
                            worksheet.write(colns[c]+str(i+9), round(float(record[c])),color_format4)
                            page_total[c] += round(float(record[c]))
                        elif c==13:
                            worksheet.write(colns[c]+str(i+9), round(float(record[c])),color_format5)
                            page_total[c] += round(float(record[c]))
                        elif c==26:
                            worksheet.write(colns[c]+str(i+9), round(float(record[c])),color_format6)
                            page_total[c] += round(float(record[c]))
                        else:
                            worksheet.write(colns[c]+str(i+9), round(float(record[c])),color_format3)
                            page_total[c] += round(float(record[c]))
                    i+=1
                    height += 50
                else:
                    worksheet.merge_range(f'A{i+9}:C{i+9}', f'Page Total of page {len(page_totals)+1}', color_format5)
                    for c in range(3,len(record),1):
                        if c in [4]:
                            worksheet.write(colns[c]+str(i+9), '',color_format5)
                        else: worksheet.write(colns[c]+str(i+9), round(float(page_total[c])),color_format5)
                    page_totals.append(page_total)
                    page_total = [0]*27
                    height = 0
                    i+=1
            if height!=0:
                worksheet.set_row(i+8, 50)
                worksheet.merge_range(f'A{i+9}:C{i+9}', f'Page Total of page {len(page_totals)+1}', color_format5)
                for c in range(3,len(record),1):
                    if c in [4]:
                        worksheet.write(colns[c]+str(i+9), '',color_format5)
                    else: worksheet.write(colns[c]+str(i+9), round(float(page_total[c])),color_format5)
                page_totals.append(page_total)

            worksheet.set_row(0, 30)
            worksheet.set_row(1, 20)
            worksheet.set_row(2, 20)
            worksheet.set_row(3, 30)
            worksheet.set_row(4, 20)
            worksheet.set_row(5, 40)
            worksheet.set_row(6, 20)
            worksheet.set_row(7, 20)

            worksheet.set_column('A:A',3)
            worksheet.set_column('C:C',12)
            
            worksheet2 = workbook.add_worksheet()
            worksheet2.merge_range('A1:Y1', 'REGULAR PAY BILL : DEFENCE CIVILIAN EMPLOYEES OF SWCCSR \n(NEW PENSION SCHEME)', color_format14)
            st = '%B %Y'
            worksheet2.merge_range('A2:Y2', f'PAGEWISE SUMMARY {datetime.datetime.today().strftime(st)}', color_format44)
            worksheet2.merge_range('A3:A6', 'S.No', color_format2)

            headers = [
                    ('ALLOWANCES', 0,3,1,11),
                    ('RECOVERY', 0, 14, 1, 13),
                    ('', 0,25,1,1),
                    ('BP', 1,3,3,1),
                    ('DEARNESS\nALLOWANCES',1,4,1,2),
                    ('DA%',2,4,2,1),
                    ('DA',2,5,2,1),
                    ('TRANSPORT\nALLOWANCE',1,6,1,2),
                    ('TPT',2,6,2,1),
                    ('DA ON\nTPT',2,7,2,1),
                    ('HRA',1,8,3,1),
                    ('WASHING\nALLOWANCE',1,9,3,1),
                    ('EXTRA\nCLAIM\n(SMALL\nFAMILY\nNORMS)',1,10,3,1),
                    ('GROSS\nENTITLEME\nNT (EXCEPT\nGMC)',1,11,3,1),
                    ('GMC% OF\n(BP+DA)',1,12,3,1),
                    ('GROSS\nENTITLEMENT',1,13,3,1),
                    ('GMC% OF\n(BP+DA)',1,14,3,1),
                    ('INDL\nCONTRI% OF\n(BP+DA)',1,15,3,1),
                    ('CGHS',1,16,3,1),
                    ('CGEIS',1,17,3,1),
                    ('LICENCE\nFEE MES\nBILLS',1,18,3,1),
                    ('OTHER\nDEDUCTION/\nFESTIVAL\nADVANCE',1,19,3,1),
                    ('INCOME\nTAX\n(PAID)',1,20,3,1),
                    ('ABSENTY/HPL/EOL DEDUCTIONS',1,21,1,4),
                    ('HPL',2,21,1,2),
                    ('EOL',2,23,1,2),
                    ('DAYS',3,21,1,1),
                    ('AMT',3,22,1,1),
                    ('DAYS',3,23,1,1),
                    ('AMT',3,24,1,1),
                    ('TOTAL\nDEDN',1,25,3,1),
                    ('AMOUNT\nPAYABLE',1,26,3,1)
                ]

            for c in range(len(headers)):

                start_row=headers[c][1]
                start_col=headers[c][2]-2
                end_row=headers[c][3]
                end_col=headers[c][4]
                starting=colns[start_col]+str(start_row+3)
                ending=colns[start_col+end_col-1]+str(start_row+end_row+2)

                if(starting==ending):
                    worksheet2.write(starting, headers[c][0],color_format2)
                else:
                    worksheet2.merge_range(f'{starting}:{ending}', headers[c][0],color_format2 )

            grand_total = [0]*27
            for rec in page_totals:
                for i,val in enumerate(rec):
                    grand_total[i]+=val
                rec[4]= ''
            grand_total[4] =''

            for r,rec in enumerate(page_totals):
                worksheet2.set_row(r+6, 40)
                for i,val in enumerate(rec):
                    if i == 0:
                        worksheet2.write(colns[0]+str(r+7), i,color_format3)
                    if i==1 or i==2:
                        continue
                    elif i in [13, 25,26]:
                        worksheet2.write(colns[i-2]+str(r+7), val,color_format2)
                    else:
                        worksheet2.write(colns[i-2]+str(r+7), val,color_format3)

            for i,val in enumerate(grand_total):
                worksheet2.set_row(len(page_totals)+6, 40)
                if i == 0:
                    worksheet2.write(colns[0]+str(len(page_totals)+7), '',color_format2)
                if i==1 or i==2:
                    continue
                elif i in [13, 25,26]:
                    worksheet2.write(colns[i-2]+str(len(page_totals)+7), val,color_format2)
                else:
                    worksheet2.write(colns[i-2]+str(len(page_totals)+7), val,color_format2)
            worksheet2.set_row(0,60)
            worksheet2.set_row(1,30)
            worksheet2.set_row(3, 40)
            workbook.close()
            # os.system('open '+file_path)
            os.startfile(file_path)
        else:
            messagebox.showerror('Error', 'Filename not given')

    @log_errors_to_file('out/errorlogs.txt')
    def columns_name(self,n):
        c=[]
        for i in range(n):
            if(i/26>=1):
                c.append(chr(ord('A')+int(i/26)-1)+chr(ord('A')+i%26))
            else:
                c.append(chr(ord('A')+i%26))
        return c

