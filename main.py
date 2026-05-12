from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from win32gui import GetForegroundWindow, GetWindowText
from uuid import uuid4
from time import sleep
from db_handeler import insert_into_table, update_values

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
    db_input['name'] = window_text[-1]
    try:
        db_input['window_title'] = window_text[-2]
    except IndexError as e:
        print(f"the following error occurred: {e}")
        db_input['window_title'] = None
        
    db_input['start_time'] = datetime.time(session.start_datetime).strftime(r"%H:%M")    
    db_input['end_time'] = datetime.time(date_time).strftime(r"%H:%M")

    db_input['date'] = datetime.date(session.start_datetime).strftime(r"%d/%m/%Y")
    db_input['duration'] = str(timedelta(seconds=session.duration))
    print(f"prepeared data to be inserted: {db_input}")
    return db_input

def prepear_update(session:ApplicationSession):
    date_time = datetime.now()
    end_time = datetime.time(date_time).strftime(r'%H:%M')
    duration = str(timedelta(seconds=session.duration))
    data = (end_time, duration, session.id)
    print(f'prepeared data to be updated: {data}')
    return data



def main():
    hwnd = GetForegroundWindow()
    app_seesion = ApplicationSession(handle=hwnd)

    while True:
        # sleep for 2 sconds to not overwhelm the cpu
        sleep(2)
        hwnd = GetForegroundWindow()
        if app_seesion.handle == hwnd:
            app_seesion.increase_duration()
            if app_seesion.duration == 2:
                insert_data = prepear_insert(app_seesion)
                insert_into_table(insert_data)
            else:
                update_data = prepear_update(app_seesion)
                update_values(update_data)
        else:
            app_seesion = ApplicationSession(handle=hwnd)



if __name__ == "__main__":
    main()