from pydantic import BaseModel, Field
from datetime import datetime
from win32gui import GetForegroundWindow, GetWindowText
from uuid import uuid4
from time import sleep
from db_handeler import insert_into_table, update_values, create_table

class ApplicationSession(BaseModel):
    # Define all fields here with type hints
    id: str = Field(default_factory=lambda: uuid4().hex)
    handle: int
    timer_step: int = 2
    duration: int = 0
    start_datetime: datetime = Field(default_factory=datetime.now)

    def increase_duration(self):
        self.duration += self.timer_step
        

def prepear_insert(session:ApplicationSession) -> dict:
    db_input = {}
    window_text = GetWindowText(session.handle).split(' - ')
    date_time = datetime.now()
    db_input['id'] = session.id
    if 'Visual Studio Code' in window_text:
        db_input['name'] = "VSCode" 
    elif "YouTube" in window_text[-1]:
        db_input['name'] = "YouTube"
    elif "Firefox" in window_text[-1]:
        db_input['name'] = 'Firefox'
    else:
        db_input['name'] = window_text[-1]
                
    try:
        db_input['window_title'] = window_text[-2]
    except IndexError as e:
        print(f"the following error occurred: {e}")
        db_input['window_title'] = None
        
    db_input['start_time'] = datetime.time(session.start_datetime).strftime(r"%H:%M")    
    db_input['end_time'] = datetime.time(date_time).strftime(r"%H:%M")

    db_input['date'] = datetime.date(session.start_datetime).strftime(r"%d/%m/%Y")
    db_input['duration'] = session.duration
    print(f"prepeared data to be inserted: {db_input}")
    return db_input

def prepear_update(session:ApplicationSession) -> tuple:
    date_time = datetime.now()
    end_time = datetime.time(date_time).strftime(r'%H:%M')
    duration = session.duration
    data = (end_time, duration, session.id)
    # print(f'prepeared data to be updated: {data}')
    return data



def main():
    hwnd = GetForegroundWindow()
    app_seesion = ApplicationSession(handle=hwnd)
    create_table()
    while True:
        # sleep for 2 sconds to not overwhelm disk I/O
        sleep(2)
        hwnd = GetForegroundWindow()
        if app_seesion.handle == hwnd:
            app_seesion.increase_duration()
            # if the session is newly created insert its data into the database
            if app_seesion.duration == app_seesion.timer_step:
                insert_data = prepear_insert(app_seesion)
                insert_into_table(insert_data)
            else:
                update_data = prepear_update(app_seesion)
                update_values(update_data)
        else:
            app_seesion = ApplicationSession(handle=hwnd)



if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"the following error occurred: {e}")