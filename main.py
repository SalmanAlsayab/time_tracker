from pydantic import BaseModel, Field
from datetime import datetime
from win32gui import GetForegroundWindow, GetWindowText
from uudi import uuid4

class ApplicationSession(BaseModel):
    # Define all fields here with type hints
    id: str = Field(default_factory=lambda: uuid4().hex)
    handle: int
    timer_step: int = 2
    duration: int = 0
    start_time: datetime = Field(default_factory=datetime.now)

    def increase_duration(self):
        self.duration += self.timer_step

# Get the handle
hwnd = GetForegroundWindow()

if __name__ == "__main__":
    # Pydantic handles the assignment automatically via keyword arguments
    app = ApplicationSession(handle=hwnd)
    
    print(f"Handle: {app.handle}")
    print(f"Start Time: {app.start_time}")
    
    app.increase_duration()
    print(f"New Duration: {app.duration}")