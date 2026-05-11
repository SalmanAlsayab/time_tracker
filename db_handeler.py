import sqlite3

con = sqlite3.connect("applications_time.db")
cur = con.cursor()

def create_table():    
    cur.execute("""CREATE TABLE applications(id CHAR(32) PRIMARY KEY, 
                DATETIME date, VARCHAR name, VARCHAR window_title,TIME start_time,TIME end_time, duration)""")
    
    



if __name__=="__main__":
    create_table()