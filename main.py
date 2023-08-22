import customtkinter
from components.sidebar import SideBar 
import sqlite3
from components.utils import *

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        con = sqlite3.connect('records.db')
        cur = con.cursor()
        if not table_exists('Personal', con):
            cur.execute('''
                        CREATE TABLE Personal (
                        id INTEGER PRIMARY KEY,
                        name varchar(255) NOT NULL,
                        rank varchar(255) NOT NULL,
                        postedat varchar(255) NOT NULL,
                        citycode varchar(255) NOT NULL,
                        doa DATE NOT NULL,
                        doi DATE NOT NULL,
                        pran varchar(255) NOT NULL)
                    ''')
            con.commit()
            
        if not table_exists('Salary', con):
            cur.execute('''
                        CREATE TABLE Salary (
                        id INTEGER,
                        month varchar(255) NOT NULL,
                        year int NOT NULL,
                        basic DOUBLE(10, 2) NOT NULL,
                        da DOUBLE(10, 2) NOT NULL,
                        tpt DOUBLE(10, 2) NOT NULL,
                        gmc DOUBLE(10, 2) NOT NULL,
                        indvc DOUBLE(10, 2) NOT NULL,
                        cgeis DOUBLE(10, 2) NOT NULL,
                        hra DOUBLE(10, 2) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (id) REFERENCES Personal(id) ON DELETE CASCADE
                    )
                    ''')
            con.commit()
        # print_table_structure('Salary', con)
        cur.close()
            
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
        self.sidebar_frame = SideBar(self,con)
        
   
if __name__ == "__main__":
    app = App()
    app.mainloop()