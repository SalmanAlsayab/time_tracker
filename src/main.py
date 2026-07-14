from pydantic import BaseModel, Field
from datetime import datetime
from win32gui import GetForegroundWindow, GetWindowText
from uuid import uuid4
from time import sleep
from .db_handeler import (
    insert_into_table,
    update_values,
    create_table,
    delete_duplicates,
)
from win32process import GetWindowThreadProcessId
import psutil
from pathlib import Path
import win32gui
import win32ui


class ApplicationSession(BaseModel):
    # Define all fields here with type hints
    id: str = Field(default_factory=lambda: uuid4().hex)
    handle: int
    timer_step: int = 2
    duration: int = 0
    start_datetime: datetime = Field(default_factory=datetime.now)

    def increase_duration(self):
        self.duration += self.timer_step


def find_exe_path(handle: int):
    thread_id, pid = GetWindowThreadProcessId(handle)
    process = psutil.Process(pid)
    exe_path = process.exe()
    return exe_path


def save_first_icon(exe_path, output_path):
    # Extract icons
    large_icons, small_icons = win32gui.ExtractIconEx(exe_path, 0)

    if not large_icons:
        return

    icon_handle = large_icons[0]

    # Create device context to draw and save the icon
    hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
    hbmp = win32ui.CreateBitmap()
    # Assuming standard 32x32 icon size,
    # use win32api.GetSystemMetrics for dynamic sizing
    hbmp.CreateCompatibleBitmap(hdc, 32, 32)

    mem_dc = hdc.CreateCompatibleDC()
    mem_dc.SelectObject(hbmp)
    mem_dc.DrawIcon((0, 0), icon_handle)

    hbmp.SaveBitmapFile(mem_dc, output_path)

    # Cleanup
    win32gui.DestroyIcon(icon_handle)


def prepear_insert(session: ApplicationSession) -> dict:
    save_icon = True
    db_input = {}
    window_text = GetWindowText(session.handle).split(" - ")
    date_time = datetime.now()
    db_input["id"] = session.id
    exe_path = find_exe_path(handle=session.handle)
    db_input["name"] = exe_path.split("\\")[-1]
    for icon in Path("icons").iterdir():
        if f"{db_input['name']}.bmp" == icon:
            save_icon = False
    if save_icon:
        save_first_icon(exe_path, f"icons/{db_input['name']}.bmp")
    try:
        db_input["window_title"] = window_text[-2]
    except IndexError as e:
        print(f"the following error occurred: {e}")
        db_input["window_title"] = None

    db_input["start_time"] = datetime.time(session.start_datetime).strftime(r"%H:%M")
    db_input["end_time"] = datetime.time(date_time).strftime(r"%H:%M")

    db_input["date"] = datetime.date(session.start_datetime).strftime(r"%Y-%m-%d")
    db_input["duration"] = session.duration
    print(f"prepeared data to be inserted: {db_input}")
    return db_input


def prepear_update(session: ApplicationSession) -> tuple:
    date_time = datetime.now()
    end_time = datetime.time(date_time).strftime(r"%H:%M")
    duration = session.duration
    data = (end_time, duration, session.id)
    # print(f'prepeared data to be updated: {data}')
    return data


def main():
    hwnd = GetForegroundWindow()
    current_session = ApplicationSession(handle=hwnd)
    next_handel = current_session.handle
    next_session = ApplicationSession(handle=0)
    strikes: int = 0
    check_duplicates_timer: int = 0
    create_table()
    while True:
        # sleep for 2 sconds to not overwhelm disk I/O
        sleep(2)
        check_duplicates_timer += 2
        hwnd = GetForegroundWindow()
        if current_session.handle == next_session.handle or strikes > 10:
            strikes = 0
            next_session = ApplicationSession(handle=0)
        if current_session.handle == hwnd:
            current_session.increase_duration()
            # if the session is newly created insert its data into the database
            if current_session.handle == next_handel:
                try:
                    insert_data = prepear_insert(current_session)
                    insert_into_table(insert_data)
                    next_handel = 0
                except Exception as e:
                    print(f"the following error occured: {e}")
            update_data = prepear_update(current_session)
            update_values(update_data)
        else:
            if strikes == 0:
                next_session = ApplicationSession(handle=hwnd)
                next_handel = next_session.handle
            elif strikes == 10 and (next_session.handle == hwnd):
                current_session = next_session
            elif strikes >= 10 and (next_session.handle != hwnd):
                current_session = ApplicationSession(handle=hwnd)
                next_handel = current_session.handle
            next_session.increase_duration()
            # current_session.increase_duration()
            strikes += 1

        if check_duplicates_timer == 60:
            delete_duplicates()
            check_duplicates_timer = 0


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"the following error occurred: {e}")
