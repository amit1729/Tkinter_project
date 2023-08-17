import tkinter
import tkinter.messagebox
import customtkinter
from components.sidebar import SideBar 
from components.newemployee import NewEmp

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

# class SideBar(customtkinter.CTkFrame):
#     def __init__(self,master):
#         super().__init__(master)

#         self.width=140
#         self.corner_radius=0
#         self.grid(row=0, column=0, rowspan=4, sticky="nsew")
#         # self.grid_rowconfigure(5, weight=1)
#         self.sidebar_button_1 = customtkinter.CTkButton(self, text='Create New Employee Record')
#         self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
#         self.sidebar_button_2 = customtkinter.CTkButton(self, text='Update Salary')
#         self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
#         self.sidebar_button_3 = customtkinter.CTkButton(self, text='Update Personal Detalis')
#         self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
#         self.sidebar_button_4 = customtkinter.CTkButton(self, text='Create Monthly Salary Report')
#         self.sidebar_button_4.grid(row=4, column=0, padx=20, pady=10)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Salary Recorder")
        self.geometry(f"{1100}x{580}")
        self.minsize(1100,580)
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        # self.grid_columnconfigure((2, 3), weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = SideBar(self)
        # create scrollable frame
        # self.scrollable_frame = NewEmp(self)

if __name__ == "__main__":
    app = App()
    app.mainloop()