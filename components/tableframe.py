import customtkinter
class CustomTable(customtkinter.CTkScrollableFrame):
    def __init__(self,master,connection):
        super().__init__(master,corner_radius=0,orientation='horizontal')
        self.con = connection
        self.grid(row=3, column=1,columnspan = 13, pady=(20,0), sticky="nsew")
        
