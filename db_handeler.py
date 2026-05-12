import sqlite3

con = sqlite3.connect("applications_time.db")
cur = con.cursor()

def create_table():    
    cur.execute("""CREATE TABLE applications(id CHAR(32) PRIMARY KEY, name VARCHAR, 
                window_title VARCHAR, start_time TIME, end_time TIME, date DATETIME, duration TIME)""")
    
def insert_into_table(data: dict):
    # Use :key_name to match the dictionary keys
    cur.execute("""
        INSERT INTO applications (id, name, window_title, start_time, end_time, date, duration) 
        VALUES (:id, :name, :window_title, :start_time, :end_time, :date, :duration)
    """, data)
    con.commit()
    
def update_values(values:tuple):
    cur.execute("UPDATE applications SET end_time = ?, duration = ? WHERE id = ?", values)
    con.commit()

if __name__=="__main__":
    create_table()