from nicegui import ui, events, app, run
import pandas as pd
import io
import tempfile
import polars as pl
from starlette.formparsers import MultiPartParser
from datetime import date
import os
#from func import main_pipeline as mp


# Get today's date as a string
today_str = date.today().strftime('%Y-%m-%d')

MultiPartParser.spool_max_size = 1024 * 1024 * 512  # 512 MB


# READ EXCEL FILE - P2
def process_excel_file(content):

    sheet_names = ['Work Task', 'Opportunity Object', 'User Object', 'WK - Provider National Account', 'WK - Provider Territories','WK - Provider Postal Code Data']
    result_dict = {}

    try:
        for sheet in sheet_names:
            try:
                with io.BytesIO(content) as f:
                        df = pl.read_excel(f, sheet_name=sheet).to_pandas()
                        if not df.empty:
                            result_dict[sheet] = df
                            print(f'✅ Loaded sheet: {sheet}, {len(df)} rows')
                        else:
                            print(f'⚠️ Sheet "{sheet}" is empty or not found')
            except Exception as e:
                print(f'❌ Failed to read sheet: {sheet} → {e}')
    
        return result_dict
    
    except Exception as e:
        ui.notify(f'Failed to parse Excel: {e}')
        print(e)


# --- Global on_connect handler for initializing tab storage ---
#@app.on_connect
#def initialize_tab_storage():
#    """Initializes app.storage.tab for each new client connection."""
#    app.storage.tab['uploaded_file'] = None
#    app.storage.tab['excel_sheets_dict'] = {}
#    app.storage.tab['file_name'] = None
#    print(f"Initialized tab storage for client: {ui.context.client.id}")


@ui.page('/')
async def main_app():

    try:
        await ui.context.client.connected(timeout=60.0) 
    except TimeoutError:
        print("Client connection timed out during page render. The browser took too long to connect.")
        ui.notify("Connection failed. Please refresh the page.", type='negative')
        return

    
    '''
    try: 
        
        await ui.context.client.connected(timeout=10.0) # Try 10 seconds or more
    except TimeoutError:
        print("Client connection timed out! This often means the browser took too long to connect.")
        ui.notify("Connection failed. Please refresh the page.", type='negative')
        return ''# Optionally, stop further execution if connection fails
    
    if ui.context.client.id not in app.storage.tab:
        # Initialize the storage for this specific tab
        app.storage.tab[ui.context.client.id] = {
            'uploaded_file': None,
            'excel_sheets_dict': {},
            'file_name': None,
        }

    
    try:
        await ui.context.client.connected(timeout=10.0) # Try 10 seconds or more
    except TimeoutError:
        print("Client connection timed out! This often means the browser took too long to connect.")
        ui.notify("Connection failed. Please refresh the page.", type='negative')
        return # Return nothing to stop further UI generation for this failed connection

    '''

    # --- Initialize app.storage.tab variables directly after connection ---
    # NiceGUI handles the per-tab isolation; you don't need to use client.id as a key here.
    # Initialize only if they don't already exist from a previous connection in the same tab
    if 'uploaded_file' not in app.storage.tab:
        app.storage.tab['uploaded_file'] = None 
    if 'excel_sheets_dict' not in app.storage.tab:
        app.storage.tab['excel_sheets_dict'] = {} 
    if 'file_name' not in app.storage.tab:
        app.storage.tab['file_name'] = None 
    
    #await ui.context.client.connected()
    #await page.wait_for_client_connection()  # <<< this line is critical

    ui.add_head_html('''
    <link href="https://fonts.googleapis.com/css2?family=Yellowtail&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;600&family=Yellowtail&display=swap" rel="stylesheet">
    <link href="https://unpkg.com/eva-icons@1.1.3/style/eva-icons.css" rel="stylesheet" />
    <link rel="stylesheet" href="https://unicons.iconscout.com/release/v4.0.8/css/line.css">
                    
    <style>
        .font-yellowtail {
            font-family: 'Yellowtail', cursive;
            font-size: .875rem;
        }
        .font-poppins {
            font-family: 'Poppins', sans-serif;
            font-size: .875rem;
        }
                    
        body{
            background-color: #FE7743;
            color: black;
        }
                    
        .q-uploader__list {
            display: none !important;
        }
                    
        .q-uploader__subtitle {
            display: none !important;
        }
                    
    </style>
    ''')


    # Header
    with ui.header().style('height: 10vh;').classes('bg-[#FE7743] text-black'):

        with ui.row().classes('items-center justify-between w-full px-6'):
            ui.button('MQL Generator') \
                .props('rounded') \
                .style('background-color: #000000; color: white;') \
                .classes('font-yellowtail normal-case')


            with ui.row().classes('gap-4 gt-sm'):
                
                ui.button('Home', on_click=lambda: ui.run_javascript(
                    "document.getElementById('home-top').scrollIntoView({ behavior: 'smooth' });"
                )).props('flat rounded').classes('text-white font-poppins font-medium normal-case')


    # PREDEFINED VALUE
    #app.storage.tab['uploaded_file'] = None 
    #app.storage.tab['excel_sheets_dict'] = {} 
    #app.storage.tab['file_name'] = None 


    uploaded_file = None
    #work_container = None  # MQL File rendering container
    file_name = None # Working File
    excel_sheets_dict = {} # for storing excel sheets
    process_button = None  # declare it globally




    ############## READ EXCEL #################

    # READ EXCEL FILE - P1
    async def excel_handler(event: events.UploadEventArguments):

        #global uploaded_file, file_name, excel_sheets_dict, spinner_container

        #file_name = event.name
        app.storage.tab['file_name'] = event.name

        file_upload_div.visible = False # if file has been successfully upload - the upload button set to hidden

        render_spinner()

        content = event.content.read()  # Read bytes

        #ui.notify(f'Reading {file_name}...')  # Confirm read works

        # Do Excel processing outside the handler
        #await run.cpu_bound(process_excel_file,content)
        #excel_sheets_dict = await run.cpu_bound(process_excel_file, content)
        #raw_bytes = await content.read()
        app.storage.tab['excel_sheets_dict'] = await run.cpu_bound(process_excel_file, content)

        #uploaded_file = excel_sheets_dict.get("Work Task")
        app.storage.tab['uploaded_file'] = app.storage.tab['excel_sheets_dict'].get("Work Task")
        

        spinner_container.clear()
        
        print(len(app.storage.tab['excel_sheets_dict']))
        print(f"📦 excel_sheets_dict after load: {list(app.storage.tab['excel_sheets_dict'].keys())}")

        render_mql_work_table()


    ############## END READ EXCEL #################


    # Render MQL Table
    def render_mql_work_table():
        #global uploaded_file, work_container, file_name, process_button
        work_container.clear()  # Remove old content if any

        if app.storage.tab['uploaded_file'] is not None:

            with work_container:

                with ui.row().classes('items-center justify-between w-full px-2 border border-black rounded-lg bg-white'):
                    
                    ui.label(app.storage.tab['file_name']).classes('text-black font-poppins font-medium normal-case')

                    with ui.row().classes('gap-4 gt-sm'):
                        process_button = ui.button('Process', on_click='').props('flat rounded').classes('text-black font-poppins font-medium normal-case')
                        process_button.visible = True
                        ui.button('Export', on_click='').props('flat rounded').classes('text-black font-poppins font-medium normal-case')
                        ui.button('Delete', on_click='').props('flat rounded').classes('text-black font-poppins font-medium normal-case')

                with ui.element('div').classes('w-[85vw] overflow-x-hidden overflow-y-auto max-h-[500px]'):
                    ui.table.from_pandas(app.storage.tab['uploaded_file'], pagination={"rowsPerPage": 50}).classes('w-full text-sm text-black').props('dense')


    # Render Loading Spinner
    def render_spinner():

        #global spinner_container

        spinner_container.clear()

        with spinner_container:
        #   with ui.element('div').style('height: 80vh;').classes('flex items-center justify-center max-w-[800px] w-full mx-auto'):
                with ui.column().classes('items-center justify-center gap-4') as spinner_div:
                    ui.spinner('dots', color='black').classes('mt-4 text-6xl')


    # Upload area
    with ui.element('div').style('height: 80vh;').classes('flex items-center justify-center max-w-[800px] w-full mx-auto'):
        with ui.column().classes('items-center justify-center gap-4') as file_upload_div:
            with ui.row():
                upload_component = ui.upload(
                    on_upload=excel_handler,#lambda e: (ui.notify(f'Uploaded {e.name}'), excel_handler(e)), # Call handle_upload here
                    on_rejected=lambda: ui.notify('Rejected!'),
                    max_file_size=1_000_000_000,
                    max_files=1,
                    auto_upload=True
                ).props('label="Browse" color=white text-color=black hide-upload-button accept=.xlsx') \
                .classes('max-w-full rounded px-4 py-2')


        # Spinner
        spinner_container = ui.column()

        # Container to update after file upload
        work_container = ui.column()



# Local deploymnet
#ui.run(port=8085, host='0.0.0.0', title='Seniority Classification', reload=False)

# Railway deploymnet
ui.run(
    host='0.0.0.0',
    port=int(os.getenv('PORT', 8080)),  # use Railway's port, fallback to 8080 locally
    title='Seniority Classification',
    reload=False
)
