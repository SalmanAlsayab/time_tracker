from pydantic import BaseModel, Field
from typing import ClassVar
from datetime import datetime
from win32gui import GetForegroundWindow, GetWindowText
from uuid import uuid4
from time import sleep
from db_handeler import (
    insert_into_table,
    update_values,
    create_table,
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
    duration: int = 0
    start_datetime: datetime = Field(default_factory=datetime.now)
    inserted: bool = False
    # Class variables
    timer_step: ClassVar[int] = 2

    def increase_duration(self):
        self.duration += self.timer_step


try:
    base_dir = Path(__file__).resolve().parent.parent
    icons_dir = base_dir / "icons"
    icons_dir.mkdir(exist_ok=True)
except FileNotFoundError:
    raise FileNotFoundError("encountered issues in icons directory")
except Exception:
    raise Exception("encountered an unexpected error")


def find_exe_path(handle: int):
    print(f"current handle = {handle}")
    thread_id, pid = GetWindowThreadProcessId(handle)
    process = psutil.Process(abs(pid))
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

    for icon in icons_dir.iterdir():
        if f"{db_input['name']}.bmp" == icon:
            save_icon = False
    if save_icon:
        save_first_icon(exe_path, f"{icons_dir / db_input['name']}.bmp")
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
    """main module that handles application tracking logic"""
    hwnd = GetForegroundWindow()
    current_session = ApplicationSession(handle=hwnd)
    next_session = ApplicationSession(handle=0)
    strikes: int = 0
    # check_duplicates_timer: int = 0
    create_table()
    while True:
        try:
            sleep(current_session.timer_step)
            hwnd = GetForegroundWindow()
            # 1 strike = 2 seconds of not using app saved in current session
            if strikes == 10:
                current_session = next_session
                next_session = ApplicationSession(handle=0)
                strikes = 0
            # make sure current session data is inserted and only once
            if not current_session.inserted:
                current_session.increase_duration()
                insert_data = prepear_insert(current_session)
                insert_into_table(insert_data)
                current_session.inserted = True

            if current_session.handle != hwnd:
                current_next_handle = next_session.handle
                next_session.increase_duration()
                if current_next_handle == 0:
                    next_session.handle = hwnd
                    strikes += 1
                elif current_next_handle == hwnd:
                    strikes += 1
                else:
                    current_session = next_session.model_copy()
                    next_session = ApplicationSession(handle=hwnd)
                    strikes = 0
            else:
                current_session.increase_duration()
                update_data = prepear_update(current_session)
                update_values(update_data)
                strikes = 0
        except psutil.NoSuchProcess as e:
            print(e)
            current_session = ApplicationSession(handle=hwnd)
            next_session = ApplicationSession(handle=0)


if __name__ == "__main__":
    main()
