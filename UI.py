from nicegui import ui, app
import sqlite3
from db_handeler import totalTime_in_application


con = sqlite3.connect('applications_time.db')
cur = con.cursor()

rows = dict(totalTime_in_application(5))


app.add_static_files('/static', 'icons')
ui.label.default_classes("text-white")
ui.icon.default_classes("pt-1 h-[1em] w-4 bg-transparent")


with ui.card().classes("items-center").classes("flex aspect-2/4 bg-violet-900/99 ring-2 ring-black/75"):
    ui.label("Top 5 most used apps").classes("pt-1")
    for key in rows.keys():
        with ui.card().classes("flex bg-rose-600/90 px-8 py-6 rounded-3xl shadow-xl/30 "):
            with ui.row():
                if key.lower() == "youtube":
                    ui.icon("img:static/youtube_icon.jpg")
                    
                if key.lower() == "vscode":
                    ui.icon("img:static/vscode_icon.png")
                
                if key.lower() == "firefox":
                    ui.icon("img:static/firefox_icon.jpg")
                
                if key.lower() == "youtube":
                    ui.icon("img:static/plex_icon.png")
                
                ui.label(f"{key}:")
                ui.label(rows[key])
ui.run()