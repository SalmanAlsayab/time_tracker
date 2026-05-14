import sqlite3

con = sqlite3.connect("applications_time.db")
con.row_factory = sqlite3.Row
cur = con.cursor()

def create_table():    
    cur.execute("""CREATE TABLE IF NOT EXISTS durationDB(id CHAR(32) PRIMARY KEY, name VARCHAR, 
                window_title VARCHAR, start_time TIME, end_time TIME, date DATETIME, duration INTEGER)""")
    con.commit()
    
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
    
def totalTime_in_application(numberOfRows:int = -1) -> list:
    cur.execute("""SELECT name, printf("%.2f hrs", (SUM(duration) / 3600.0)) AS total_duration
      FROM durationDB
      GROUP BY name
      HAVING SUM(duration) > 60
      ORDER BY total_duration DESC
      """)
    if numberOfRows == -1:
        return cur.fetchall()
    
    return cur.fetchmany(numberOfRows)


if __name__=="__main__":
    # create_table()
    pass