from nicegui import ui, app
from db_handeler import totalTime_in_application, user_history, app_history, top5_daily, top5_weekly
from main import main
from threading import Thread
app.add_static_files('/static', 'icons')
# ui.label.default_classes("text-white")
ui.icon.default_classes("absolute left-3 right-5 ")



def render_buttons(query_output:list):
    rows = dict(query_output)
    request = ui.context.client.request
    if request.url.path != "/all_apps":
        with ui.grid(columns="auto").classes("absolute left-15 top-14 bg-red-100 no-border"):
            ui.select(options=['daily', 'weekly', 'all time'], with_input=True, 
            on_change=lambda e: ui.navigate.to(f'/{e.value}') if e.value != 'all time' else ui.navigate.to('/')).classes("")

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

@ui.page("/app_page/{app_name}")
def app_page(app_name:str):
    app.native.main_window.resize(500, 540)
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
    with ui.grid(columns="auto auto auto"):
        ui.input('Search by name/time/date').bind_value(table, 'filter').classes('w-60')
        ui.label("").classes('w-28')
        ui.button(icon='home', on_click= lambda: ui.navigate.to('/')).classes("items-center bg-sky-500")


@ui.page("/history")
def full_history():
    app.native.main_window.resize(555, 540)
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
    with ui.grid(columns="auto auto auto"):
        ui.input('Search by name/time/date').bind_value(table, 'filter').classes('w-60')
        ui.label("").classes('w-48')
        ui.button(icon='home', on_click= lambda: ui.navigate.to('/')).classes("items-center bg-sky-500")
   

@ui.page('/all_apps')
def show_all_apps():
    app.native.main_window.resize(365, 605)
    with ui.card().classes("flex items-center h-134 w-80  bg-red-100 ring-2 ring-black/75"):
        with ui.scroll_area().classes("h-110 w-75 "): 
            render_buttons(totalTime_in_application())
        ui.link('Show full history', '/history').classes('text-sky-600 font-bold text-lg no-underline')


@ui.page('/')
def main_page():
    app.native.main_window.resize(340, 560)
    with ui.card().classes("flex items-center h-auto w-auto bg-red-100 ring-2 ring-black/75 "):
        ui.label("Top 5 most used apps").classes("pt-1 text-sky-600 font-bold text-xl")
        ui.label("").classes("pt-5")


        render_buttons(totalTime_in_application(5))
        ui.link('Show more apps','/all_apps').classes('text-sky-600 font-bold text-lg no-underline')

@ui.page('/daily')
def daily():
    app.native.main_window.resize(340, 560)
    with ui.card().classes("flex items-center h-auto w-auto bg-red-100 ring-2 ring-black/75 "):
        ui.label("most used apps today").classes("pt-1 text-sky-600 font-bold text-xl")
        ui.label("").classes("pt-5")


        render_buttons(top5_daily())
        ui.link('Show more apps','/all_apps').classes('text-sky-600 font-bold text-lg no-underline')

@ui.page('/weekly')
def weekly():
    app.native.main_window.resize(340, 560)
    with ui.card().classes("flex items-center h-auto w-auto bg-red-100 ring-2 ring-black/75 "):
        ui.label("most used apps this week").classes("pt-1 text-sky-600 font-bold text-xl")
        ui.label("").classes("pt-5")


        render_buttons(top5_weekly())
        ui.link('Show more apps','/all_apps').classes('text-sky-600 font-bold text-lg no-underline')


app.native.window_args['resizable'] = False

def start_backend():
    main()

Thread(target=start_backend, daemon=True).start()

ui.run(native=True, window_size=(340, 560), fullscreen=False)


