import sqlite3

def get_connection():
    con = sqlite3.connect("applications_time.db")
    con.execute('PRAGMA journal_mode=WAL;')
    con.row_factory = sqlite3.Row
    return con


def create_table():    
    with get_connection() as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS durationDB(id CHAR(32) PRIMARY KEY, name VARCHAR, 
                    window_title VARCHAR, start_time TIME, end_time TIME, date DATETIME, duration INTEGER)""")
        con.commit()
    
def delete_table(table_name: str):
    with get_connection() as con:
        cur = con.cursor()
        cur.execute(f"DROP TABLE {table_name}" )
        con.commit()
        
def insert_into_table(data: dict):
    with get_connection() as con:
        cur = con.cursor()
        # Use :key_name to match the dictionary keys
        cur.execute("""
            INSERT INTO durationDB (id, name, window_title, start_time, end_time, date, duration) 
        VALUES (:id, :name, :window_title, :start_time, :end_time, :date, :duration)""", data)
        con.commit()
    
def update_values(values:tuple):
    with get_connection() as con:
        cur = con.cursor()
        cur.execute("UPDATE durationDB SET end_time = ?, duration = ? WHERE id = ?", values)
        con.commit()
        
def totalTime_in_application(numberOfRows:int = -1) -> list:
    with get_connection() as con:
        cur = con.cursor()
        cur.execute("""SELECT name, (SUM(duration) / 3600.0) AS total_duration
        FROM durationDB
        WHERE name <> ''
        GROUP BY name
      HAVING SUM(duration) > 60
      ORDER BY total_duration DESC""")
    if numberOfRows == -1:
        return cur.fetchall()
    return cur.fetchmany(numberOfRows)
    
    
def app_history(app_name: str):
    with get_connection() as con:
        cur = con.cursor()
        cur.execute(""" SELECT id, date, start_time, end_time, duration 
                        FROM durationDB
                        WHERE name = ? 
                        ORDER BY date DESC, start_time DESC""", (app_name,))
    return cur.fetchall()

def user_history():
    with get_connection() as con:
        cur = con.cursor()
        cur.execute(""" SELECT id, name, start_time, end_time, date, duration 
                    FROM durationDB
                    WHERE name <> ''
                    ORDER BY date DESC, start_time DESC""")
    return cur.fetchall()

def delete_duplicates():
    with get_connection() as con:
        cur = con.cursor()
        cur.execute("""DELETE FROM durationDB
                WHERE rowid NOT IN (
                    SELECT MIN(rowid)
                    FROM durationDB
                    GROUP BY name, date, start_time, end_time, duration
);""")
        
def top5_daily():
    with get_connection() as con:
        cur = con.cursor()
        cur.execute("""SELECT name, (SUM(duration) / 3600.0) AS total_duration
                    FROM durationDB
                    WHERE name <> '' AND date = DATE('now')
                    GROUP BY name
                    ORDER BY total_duration DESC""")
        return cur.fetchmany(5)
    
def top5_weekly():
    with get_connection() as con:
        cur = con.cursor()
        cur.execute("""SELECT name, (SUM(duration) / 3600.0) AS total_duration
                    FROM durationDB
                    WHERE name <> '' AND date BETWEEN DATE('now', 'weekday 0', '-7 days') 
                    AND DATE('now', 'weekday 0', '-1 days') 
                    GROUP BY name
                    ORDER BY total_duration DESC""")
        return cur.fetchmany(5)
    
def clean_date():
    with get_connection() as con:
        cur = con.cursor()
        cur.execute("""UPDATE durationDB 
                    SET date = SUBSTR(date, 7, 4) || '-' || SUBSTR(date, 4, 2) || '-' ||SUBSTR(date, 1, 2)""")
        
def clean():
    with get_connection() as con:
        cur = con.cursor()
        cur.execute("""UPDATE durationDB
                    SET name = 'Code.exe' 
                    WHERE name = 'code.exe'""")
if __name__=="__main__":
    # clean()       
    pass