import sqlite3

con = sqlite3.connect("applications_time.db")
cur = con.cursor()

def create_table():    
    cur.execute("""CREATE TABLE IF NOT EXISTS durationDB(id CHAR(32) PRIMARY KEY, name VARCHAR, 
                window_title VARCHAR, start_time TIME, end_time TIME, date DATETIME, duration INTEGER)""")
def delete_table(table_name: str):
    cur.execute(F"DROP TABLE {table_name}" )
    con.commit()
def insert_into_table(data: dict):
    # Use :key_name to match the dictionary keys
    cur.execute("""
        INSERT INTO durationDB (id, name, window_title, start_time, end_time, date, duration) 
        VALUES (:id, :name, :window_title, :start_time, :end_time, :date, :duration)
    """, data)
    con.commit()
    
def update_values(values:tuple):
    cur.execute("UPDATE durationDB SET end_time = ?, duration = ? WHERE id = ?", values)
    con.commit()
    
def totalTime_in_application() -> list:
    cur.execute("""
        SELECT name, printf('%d:%02d:%02d',
            SUM(
                CAST(substr(duration, 1, 2) AS INTEGER) * 3600 +
                CAST(substr(duration, 3, 2) AS INTEGER) * 60 +
                CAST(substr(duration, 6, 2) AS INTEGER)
            ) / 3600,
            (SUM(
                CAST(substr(duration, 1, 2) AS INTEGER) * 3600 +
                CAST(substr(duration, 3, 2) AS INTEGER) * 60 +
                CAST(substr(duration, 6, 2) AS INTEGER)
            ) % 3600) / 60,
            SUM(
                CAST(substr(duration, 1, 2) AS INTEGER) * 3600 +
                CAST(substr(duration, 3, 2) AS INTEGER) * 60 +
                CAST(substr(duration, 6, 2) AS INTEGER)
            ) % 60
        ) AS t
        FROM applications
        GROUP BY name
        ORDER BY t DESC
        
    """)
    con.commit()
    return cur.fetchall()
if __name__=="__main__":
    create_table()
