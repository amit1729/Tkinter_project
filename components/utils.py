import datetime
from tkinter import messagebox
def validDate(date):
    dateFormat = '%d/%m/%Y'
    try:
        date = date.split('/')
        if len(date[0])==1: date[0] = '0'+date[0]
        if len(date[1])==1: date[1] = '0'+date[1]
        date = '/'.join(date)
        dateObject = datetime.datetime.strptime(date, dateFormat)
        return True
    except:
        return False

def chageFormat(date, _from, to):
    dt = datetime.datetime.strptime(date, _from)
    return dt.strftime(to)

def validPercent(num):
    try:
        num = float(num)
        if num <=100 and num >=0:
            return True
        else:
            return False
    except:
        return False

def validAmount(num):
    try:
        num = float(num)
        return True
    except:
        return False

def validNumber(number):
    # print(len(number))
    try:
        # print(number)
        int(number)
    except:
        return False
    return True

def table_exists( table_name, connection):
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    res = cursor.fetchone() is not None
    cursor.close()
    return res

def print_table_structure(table_name, connection):
    cursor = connection.cursor()
    
    # Get the table structure
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    
    print(f"Structure of table '{table_name}':")
    print("Column Name | Data Type         | Constraints")
    print("-" * 50)
    for column in columns:
        constraints = ""
        if column[5] == 1:
            constraints += "PRIMARY KEY "
        if column[3] == 1:
            constraints += "NOT NULL "
        if column[4] == 1:
            constraints += "UNIQUE "
        
        # Check for foreign key constraints
        cursor.execute(f"PRAGMA foreign_key_list({table_name})")
        foreign_keys = cursor.fetchall()
        for fk in foreign_keys:
            if fk[3] == column[1]:
                constraints += f"FOREIGN KEY ({fk[3]}) REFERENCES {fk[2]}({fk[4]}) "
        
        print(f"{column[1]:12} | {column[2]:16} | {constraints}")
    
    print("\n")


def log_errors_to_file(file_path):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                with open(file_path, 'a') as f:
                    timestamp = datetime.datetime.now().strftime("[%d/%m/%Y %H:%M:%S]")
                    class_name = args[0].__class__.__name__
                    error_message = f"{timestamp} {class_name}.{func.__name__}:\n{e}\n"
                    f.write(error_message)
                messagebox.showerror('Internal Error', 'Some error occured please see log file for more details')
        return wrapper
    return decorator

def runtimelog(idx, file_path = 'out/RuntimeLog.txt'):
    with open(file_path, 'a') as f:
        timestamp = datetime.datetime.now().strftime("[%d/%m/%Y %H:%M:%S]")
        message = f"{timestamp} Records for person number {idx} for the given month is not found hence using closest available data"
        f.write(message)
