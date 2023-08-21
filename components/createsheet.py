import customtkinter
from tkinter import *
import datetime
from functools import partial
from .utils import chageFormat
from tkinter import messagebox, filedialog
import xlsxwriter
import os
# from .tableframe import CustomTable

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

        self.monthList = ['January', 'Febuary', 'March', 'April','May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
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
        # self.textbox.insert('0.0', f'Name: {self.name.get()}\nDate of Birth: {self.dob.get()}\nCO: {self.co.get()}\nRank: {self.rank.get()}\nMobile Number: {self.mobno.get()}')
        # self.textbox.configure(state = 'hidden')
        self.searchButton = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"),hover_color='green', text='Add',height = 80, command=self.addButtonClicked)
        # self.searchButton.configure(state = 'hidden')
        self.searchButton.grid(row=2, column=8, columnspan = 3, padx=(20, 20), pady=(20, 20), sticky="ew")
        
        self.exportButton = customtkinter.CTkButton(master=self, border_width=2, text_color=("gray10", "#DCE4EE"), text='Export',height = 80, command=self.exportButtonClicked)
        self.exportButton.grid(row=2, column=11, columnspan = 3, padx=(20, 20), pady=(20, 20), sticky="ew")
        # self.exportButton.configure(state = 'hidden')
        # self.tableFrame = CustomTable(self,self.con)
        
    def enterPressed(self,event):
        self.searchButtonClicked()

    def _ctsv(self,x):
        return StringVar(value=str(x))
    
    

    def fetchPersonalDetails(self):
        cur = self.con.cursor()
        res = cur.execute("SELECT * FROM Personal WHERE id = ?",
               (self.snoEntry.get(),))
        row = res.fetchone()
        cur.close()
        flag = not row == None
        return row, flag
    
    def searchButtonClicked(self):
        data, exists = self.fetchPersonalDetails()
        if exists:
            self.name = self._ctsv(data[1])
            self.dob = self._ctsv(chageFormat(data[2], '%Y-%m-%d','%d/%m/%Y' ))
            self.co = self._ctsv(data[3])
            self.rank = self._ctsv(data[4])
            self.mobno = self._ctsv(data[5])
            # self.textbox = customtkinter.CTkTextbox(master=self,height = 100, width = 150)
            # self.textbox.grid(row=2, column=1, columnspan = 7,padx=(20, 20), pady=(20, 20), sticky="nsew")
            self.textbox.insert('0.0', f'Name: {self.name.get()}\nDate of Birth: {self.dob.get()}\nCO: {self.co.get()}\nRank: {self.rank.get()}\nMobile Number: {self.mobno.get()}')
            self.textbox.configure(state = 'disabled')
            # self.searchButton.configure(state = 'normal')
            # self.exportButton.configure(state = 'normal')
            # self.searchButton = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"),hover_color='green', text='Add',height = 80, command=self.addButtonClicked)
            # self.searchButton.grid(row=2, column=8, columnspan = 3, padx=(20, 20), pady=(20, 20), sticky="ew")
            # self.exportButton = customtkinter.CTkButton(master=self, border_width=2, text_color=("gray10", "#DCE4EE"), text='Export',height = 80, command=self.exportButtonClicked)
            # self.exportButton.grid(row=2, column=11, columnspan = 3, padx=(20, 20), pady=(20, 20), sticky="ew")
        else:
            messagebox.showerror('Not Found', f'Empolyee with serial number {self.snoEntry.get()} does not exists')

    def disable(self, widgt):
        widgt.configure(state = 'disable')

    def fetchSalary(self):
        cur = self.con.cursor()
        # print(f'SELECT * FROM Salary WHERE id = {self.snoEntry.get()} AND month = {self.monthOptionMenu.get().upper()} AND year = {self.yearOptionMenu.get()}')
        res = cur.execute("SELECT * FROM Salary WHERE id = ? AND month = ? AND year = ?",
               (self.snoEntry.get(),self.monthOptionMenu.get().upper(),self.yearOptionMenu.get()))
        row = res.fetchall()
        # print(row)
        cur.close()
        if len(row) > 1:
            print(row)
            messagebox.showwarning('Multiple Entries', f'Multiple Entries Found')
        flag = not len(row) == 0
        if flag: return row[0], flag
        else: return None,flag

    def calPercent(self,base, percent):
        return str(round(float(base)*float(percent)/100,2))

    def createRecord(self):
        salData, salExists = self.fetchSalary()
        if salExists:
            basicPay = salData[3]
            da = salData[4]
            tda = salData[5]
            daontda = salData[6]
            deductions = salData[7]
            hra = salData[8]
            monthVar = salData[1]
            yearVar = salData[2]
            record = [
                    self.snoEntry.get(),
                    f'Name: {self.name.get()}\nDate of Birth: {self.dob.get()}\nCO: {self.co.get()}\nRank: {self.rank.get()}\nMobile Number: {self.mobno.get()}',
                    'Details\nHere\nOkay',
                    basicPay,
                    da,
                    self.calPercent(basicPay,da),
                    # hra,
                    tda,
                    # daontda,
                    self.calPercent(tda,da),
                    self.calPercent(basicPay,hra),
                    '0',
                    '0',
                    '0',
                    '0',
                    '0',
                    '0',
                    '0',
                    '0',
                    '0',
                    '0',
                    '0',
                    '0',
                    '0',
                    '0',
                    '0',
                    '0',
                    deductions,
                    str(round(float(basicPay)+float(self.calPercent(basicPay,hra))+float(self.calPercent(basicPay,da))+float(tda)+float(self.calPercent(tda,daontda))-float(deductions), 2))
                    ]
            return record, True
        else:
            messagebox.showerror('Not Found', f'Salary record for Empolyee with serial number {self.snoEntry.get()} for the month of {self.monthOptionMenu.get()} {self.yearOptionMenu.get()} does not exists')
        return None, False
    

    def buildHeader(self):
        self.headers = [
            ('S.No', 0, 0, 4, 1),
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
            ('GMC\n10% OF\n(BP+GP+DA)',1,12,3,1),
            ('GROSS\nENTITLEMENT',1,13,3,1),
            ('GMC\n10% OF\n(BP+GP+DA)',1,14,3,1),
            ('INDL\nCONTRI\n10% OF\n(BP+GP+DA)',1,15,3,1),
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
            ('ACTION', 0, 27,4,1)
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
            self.ele = customtkinter.CTkLabel(master=self.tableFrame,text=header[0], corner_radius=2,font=customtkinter.CTkFont(size=12, weight='bold'),bg_color='#2b2b2b',padx  = 15)
            self.ele.grid(row=header[1], column=header[2],rowspan = header[3], columnspan = header[4] ,padx=(1,1), pady=(1,1),sticky="nsew")
            # self.ele.insert(END, header[0],"center")

    def addButtonClicked(self):
        if self.snoEntry.get == '' or self.snoEntry.get() in self.entryIds.values():
            messagebox.showerror('Duplication', f'Record of the empolyee with serial number {self.snoEntry.get()} already exists in the table')
            return
        self.searchButtonClicked()
        record, exists = self.createRecord()
        if exists:
            
            if self.index == 0:
                self.buildHeader()
                # self.height = 30
                # self.tableFrame = customtkinter.CTkScrollableFrame(self,corner_radius=0,orientation='horizontal')
                # self.tableFrame.grid(row=3, column=1,columnspan = 13, pady=(20,0), sticky="nsew")
                # for i, header in enumerate(self.headers):
                #     self.ele = customtkinter.CTkEntry(self.tableFrame,corner_radius=0,font=customtkinter.CTkFont(size=11))
                #     self.ele.grid(row = self.index+3, column = i+1, sticky = 'snew')
                #     self.ele.insert(END, header)
                #     self.disable(self.ele)
            self.height+=70
            self.tableFrame.configure(height = self.height)
            elements = []
            for i, rec in enumerate(record):
                if i == 1 or i==2:
                    self.ele = customtkinter.CTkTextbox(master=self.tableFrame,height = 70,corner_radius=0,font=customtkinter.CTkFont(size=12))
                    self.ele.grid(row=self.index+4, column=i, sticky="nsew")
                    self.ele.insert(END,rec)
                    elements.append(self.ele)
                    self.disable(self.ele)
                else:
                    self.ele = customtkinter.CTkEntry(master=self.tableFrame,corner_radius=0,font=customtkinter.CTkFont(size=12))
                    self.ele.grid(row=self.index+4, column=i, sticky="nsew")
                    self.ele.insert(END,rec)
                    elements.append(self.ele)
                    self.disable(self.ele)
            self.deleteButton = customtkinter.CTkButton(master=self.tableFrame, fg_color="transparent", border_width=2,hover_color='red', text_color=("gray10", "#DCE4EE"), text='Remove', command=partial(self.deleteButtonClicked, self.index),font=customtkinter.CTkFont(size=12, weight='bold'))
            self.deleteButton.grid(row=self.index+4, column=i+1, padx=(5, 5),pady = (5,5), sticky="nsew")
            elements.append(self.deleteButton)
            self.entries[self.index] = (elements, record)
            self.entryIds[self.index] = record[0]
            self.index+=1
            

    def deleteButtonClicked(self, i):
        for ele in self.entries[i][0]:
            ele.destroy()
        del self.entries[i]
        del self.entryIds[i]
        if len(self.entries)==0:
            self.tableFrame.destroy()
            self.index = 0
        self.height-=70
        self.tableFrame.configure(height = self.height)

    def exportButtonClicked(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Workbook", "*.xlsx"), ],
            title="Save As"
            )
        if file_path:
            workbook = xlsxwriter.Workbook(file_path)
            worksheet = workbook.add_worksheet()
            worksheet.set_row(1, 20)
            worksheet.set_row(2, 20)
            worksheet.merge_range('C2:I3', f'Salary Report for the month of {self.monthOptionMenu.get()} {self.yearOptionMenu.get()}', cell_format=workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter','font_size': 15,'font_name': 'Times New Roman'}))
            worksheet.set_column('B:B', 30)
            x = 0
            header_format = workbook.add_format({'bold': True, 'font_size': 11,'font_name': 'Times New Roman', 'align': 'center', 'valign': 'vcenter'})
            # Write content with the specified font size
            colns = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            for c in range(len(self.headers)-1):
                if colns[c]!='B':
                    worksheet.set_column(f'{colns[c]}:{colns[c]}', 15)
                worksheet.write(colns[c]+str(5), self.headers[c], header_format)

            records = list(map(lambda x: x[1], self.entries.values()))
            records.sort(key = lambda x: x[0])
            # print(records)
            entry_format = workbook.add_format({'bold': False, 'font_size': 11,'font_name': 'Times New Roman', 'text_wrap': True,  'valign': 'vcenter'})
            for i, record in enumerate(records):
                worksheet.set_row(i+5, 90)
                colns = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                for c in range(len(record)):
                    if c == 1:
                        worksheet.write(colns[c]+str(i+6), record[c], entry_format)
                    elif c==0:
                        worksheet.write(colns[c]+str(i+6), int(record[c]), entry_format)
                    else:
                        worksheet.write(colns[c]+str(i+6), float(record[c]), entry_format)
            workbook.close()
            os.system('start '+file_path)
        else:
            messagebox.showerror('Error', 'Filename not given')

