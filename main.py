from pydantic import BaseModel
from win32gui import GetForegroundWindow, GetWindowText
import re
import time
from datetime import datetime
class application(BaseModel):
    def __init__(self, name:str):
        self.name = name
        self.timer_step:int = 2
        self.timer:int = 0
        
        def increase_timer():
            self.timer += self.timer_step
            
time.sleep(2)
# Get the handle to the foreground window
hwnd = GetForegroundWindow()

# Get the text (title) of that window
window_title = GetWindowText(hwnd)
print(f"Active Window: {window_title.split('-')}")


            