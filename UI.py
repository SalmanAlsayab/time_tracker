from nicegui import ui, app
from db_handeler import totalTime_in_application, user_history, app_history
app.add_static_files('/static', 'icons')
# ui.label.default_classes("text-white")
ui.icon.default_classes("absolute left-3 right-5 ")


@ui.page("/app_page/{app_name}")
def app_page(app_name:str):

    table = ui.table(
        columns=[
            {'name': 'date', 'label': 'date', 'field': 'date', 'align': 'middle', 'sortable': True},
            {'name': 'start_time', 'label': 'start_time', 'field': 'start_time', 'align': 'left', 'sortable': True},
            {'name': 'end_time', 'label': 'end_time', 'field': 'end_time', 'align': 'left', 'sortable': True},
            {'name': 'duration', 'label': 'duration', 'field': 'duration', 'align': 'left', 'sortable': True, ':format': 'value => value + " secs"'},
        ],
        rows=[dict(row) for row in app_history(app_name=app_name)],
        row_key='id',
        pagination=5,column_defaults={'align': 'left', 'headerClasses': 'uppercase text-primary',
}).classes("items-center bg-red-100 text-sky-500 text-xl font-medium border-separate border-black opacity-80 ring-2 ring-black/75")
    with table.add_slot('top'):
        ui.label(f"{app_name}'s history ").classes("text-sky-500 font-bold text-xl")
    ui.input('Search by time/date').bind_value(table, 'filter')


@ui.page("/history")
def full_history():

    table = ui.table(
        columns=[   
            {'name': 'name', 'label': 'name', 'field': 'name', 'align': 'middle', 'sortable': True},
            {'name': 'date', 'label': 'date', 'field': 'date', 'align': 'middle', 'sortable': True},
            {'name': 'start_time', 'label': 'start_time', 'field': 'start_time', 'align': 'left', 'sortable': True},
            {'name': 'end_time', 'label': 'end_time', 'field': 'end_time', 'align': 'left', 'sortable': True},
            {'name': 'duration', 'label': 'duration', 'field': 'duration', 'align': 'left', 'sortable': True, ':format': 'value => value + " secs"'},
        ],
        rows=[dict(row) for row in user_history()],
        row_key='id',
        pagination=5,column_defaults={'align': 'left', 'headerClasses': 'uppercase text-primary',
}).classes("items-center bg-red-100 text-sky-500 text-xl font-medium border-separate border-black opacity-80 ring-2 ring-black/75")
    with table.add_slot('top'):
        ui.label("Full history ").classes("text-sky-500 font-bold text-xl")
    ui.input('Search by name/time/date').bind_value(table, 'filter')
   
   

@ui.page('/all_apps')
def show_all_apps():
    rows = dict(totalTime_in_application())
    with ui.card().classes("flex items-center h-134 w-80  bg-red-100 ring-2 ring-black/75"):
        with ui.scroll_area().classes("h-110 w-75 "): 
            for key in rows.keys():
                with ui.button(on_click=lambda key=key: ui.navigate.to(f'/app_page/{key}')).classes("flex w-65 h-15 bg-skyblue px-8 py-6 rounded-3xl shadow-xl/30 opacity-80"):
                    with ui.grid(columns="1px auto auto").classes("pb-8"):
                        if key.lower() == "youtube":
                            ui.icon("img:static/youtube.png").classes(" ")
                            
                        elif key.lower() == "vscode":
                            ui.icon("img:static/vscode_icon.png")
                        
                        elif key.lower() == "firefox":
                            ui.icon("img:static/firefox.png")
                        
                        elif key.lower() == "plex":
                            ui.icon("img:static/plex_icon.png")
                        else:
                            ui.icon("img:static/windows.png")
                        if len(key.split()) >= 2:
                            ui.label(f"{key.split()[0]}").classes("absolute left-10 right-auto text-white")
                        else:
                            ui.label(f"{key}").classes("absolute left-10 right-auto text-white")                        
                        ui.label(f'{rows[key]:.2f} hrs' ).classes(" w-30 pl-10 text-white")
        ui.link('Show full history', '/history').classes('text-sky-600 font-bold text-lg no-underline')

@ui.page('/')
def main_page():
    rows = dict(totalTime_in_application(5))
    with ui.card().classes("flex items-center h-auto w-auto  bg-red-100 ring-2 ring-black/75"):
        ui.label("Top 5 most used apps").classes("pt-1 text-sky-600 font-bold text-xl")
        for key in rows.keys():
            with ui.button(on_click=lambda key=key: ui.navigate.to(f'/app_page/{key}')).classes("flex w-65 h-15 bg-skyblue px-8 py-6 rounded-3xl shadow-xl/30 opacity-80"):
                with ui.grid(columns="1px auto auto").classes("pb-8"):
                    if key.lower() == "youtube":
                        ui.icon("img:static/youtube.png").classes(" ")
                        
                    elif key.lower() == "vscode":
                        ui.icon("img:static/vscode_icon.png")
                    
                    elif key.lower() == "firefox":
                        ui.icon("img:static/firefox.png")
                    
                    elif key.lower() == "plex":
                        ui.icon("img:static/plex_icon.png")
                    else:
                        ui.icon("img:static/windows.png")
                    if len(key.split()) >= 2:
                        ui.label(f"{key.split()[0]}").classes("absolute left-10 right-auto text-white")
                    else:
                        ui.label(f"{key}").classes("absolute left-10 right-auto text-white")                        
                    ui.label(f'{rows[key]:.2f} hrs').classes(" w-30 pl-10 text-white")
        ui.link('Show more apps','/all_apps').classes('text-sky-600 font-bold text-lg no-underline')

ui.run()