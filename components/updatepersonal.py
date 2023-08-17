import customtkinter

class UpdatePersonal(customtkinter.CTkScrollableFrame):
    def __init__(self,master):
        super().__init__(master, label_text='Update Personal Details')

        self.grid(row=0, column=1,rowspan=4, padx=(20, 0), pady=(20,0), sticky="nsew")
        
