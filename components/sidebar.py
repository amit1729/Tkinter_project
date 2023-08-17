import customtkinter
from .createsheet import CreateSheet
from .updatepersonal import UpdatePersonal
from .updatesal import UpdateSalary
from .newemployee import NewEmp

class SideBar(customtkinter.CTkFrame):
    def __init__(self,master):
        super().__init__(master)
        self.master = master
        self.master.current = UpdateSalary(self.master)
        self.width=140
        self.corner_radius=0
        self.grid(row=0, column=0, rowspan=4, padx=(5, 0), pady=(20,0), sticky="nsew")
        # self.grid_rowconfigure(5, weight=1)
        self.sidebar_button_1 = customtkinter.CTkButton(self, text='Create New Employee Record', command=self._new_emp)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self, text='Update Salary',command=self._update_salary)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self, text='Update Personal Detalis', command=self._update_personal)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.sidebar_button_4 = customtkinter.CTkButton(self, text='Create Monthly Salary Report', command=self._create_sheet)
        self.sidebar_button_4.grid(row=4, column=0, padx=20, pady=10)
        # self.appearance_mode_label = customtkinter.CTkLabel(self, text="Appearance Mode:", anchor="w")
        # self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))
        # self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self, values=["Light", "Dark", "System"],
        #                                                                command=self.change_appearance_mode_event)
        # self.appearance_mode_optionemenu.grid(row=7, column=0, padx=20, pady=(10, 10))
        # self.scaling_label = customtkinter.CTkLabel(self, text="UI Scaling:", anchor="w")
        # self.scaling_label.grid(row=8, column=0, padx=20, pady=(10, 0))
        # self.scaling_optionemenu = customtkinter.CTkOptionMenu(self, values=["80%", "90%", "100%", "110%", "120%"],
        #                                                        command=self.change_scaling_event)
        # self.scaling_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 20))
    def _new_emp(self):
        self.master.current.destroy()
        self.master.current = NewEmp(self.master)
    def _update_salary(self):
        self.master.current.destroy()
        self.master.current = UpdateSalary(self.master)
    def _update_personal(self):
        self.master.current.destroy()
        self.master.current = UpdatePersonal(self.master)
    def _create_sheet(self):
        self.master.current.destroy()
        self.master.current = CreateSheet(self.master)

    
 
