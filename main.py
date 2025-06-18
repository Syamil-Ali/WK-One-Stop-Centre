from nicegui import ui, events, app, run
from starlette.formparsers import MultiPartParser
from datetime import date
import os

# layout
import layout.custom_html as ch
import layout.header as header

# function
import function as func


# Get today's date as a string
today_str = date.today().strftime('%Y-%m-%d')

MultiPartParser.spool_max_size = 1024 * 1024 * 512  # 512 MB



@ui.page('/')
async def main_app():


    try:
        await ui.context.client.connected(timeout=60.0) # <<< this line is critical
    except TimeoutError:
        print("Client connection timed out during page render. The browser took too long to connect.")
        ui.notify("Connection failed. Please refresh the page.", type='negative')
        return


    # --- Initialize app.storage.tab variables directly after connection ---
    # NiceGUI handles the per-tab isolation; you don't need to use client.id as a key here.
    # Initialize only if they don't already exist from a previous connection in the same tab
    if 'uploaded_file' not in app.storage.tab:
        app.storage.tab['uploaded_file'] = None 
    if 'excel_sheets_dict' not in app.storage.tab:
        app.storage.tab['excel_sheets_dict'] = {} 
    if 'file_name' not in app.storage.tab:
        app.storage.tab['file_name'] = None 
    

    # Add Custom HTML
    ch.custom_html()

    # Header
    header.header()


    # UPLOAD AND READ EXCEL
    async def excel_handler(event: events.UploadEventArguments):

        file_upload_div.visible = False # if file has been successfully upload - the upload button set to hidden
        
        app.storage.tab['file_name'] = event.name

        render_spinner()

        content = event.content.read()  # Read bytes

        #ui.notify(f'Reading {file_name}...')  # Confirm read works

        # Do Excel processing outside the handler
        app.storage.tab['excel_sheets_dict'] = await run.io_bound(func.read_excel_sheets, content)

        #uploaded_file = excel_sheets_dict.get("Work Task")
        app.storage.tab['uploaded_file'] = app.storage.tab['excel_sheets_dict'].get("Work Task")
        

        spinner_container.clear()
        
        print(len(app.storage.tab['excel_sheets_dict']))
        print(f"📦 excel_sheets_dict after load: {list(app.storage.tab['excel_sheets_dict'].keys())}")

        render_mql_work_table()


    ############## END READ EXCEL #################


    # Render MQL Table
    def render_mql_work_table():
        
        work_container.clear()  # Remove old content if any

        if app.storage.tab['uploaded_file'] is not None:

            with work_container:
                
                # Show File Option
                with ui.row().classes('items-center justify-between w-full px-2 border border-black rounded-lg bg-white'):
                    
                    ui.label(app.storage.tab['file_name']).classes('text-black font-poppins font-medium normal-case')

                    with ui.row().classes('gap-4 gt-sm'):
                        process_button = ui.button('Process', 
                                                   on_click= lambda: func.start_process_mql(work_container, render_spinner, spinner_container, render_mql_work_table, process_button)
                                                   ).props('flat rounded').classes('text-black font-poppins font-medium normal-case')
                        process_button.visible = True
                        ui.button('Export', on_click= lambda: func.export_mql_work(app.storage.tab['uploaded_file'], today_str)).props('flat rounded').classes('text-black font-poppins font-medium normal-case')
                        ui.button('Delete', on_click= lambda: func.delete_mql_work(upload_component, file_upload_div, work_container)).props('flat rounded').classes('text-black font-poppins font-medium normal-case')

                # Show Table
                with ui.element('div').classes('w-[85vw] overflow-x-hidden overflow-y-auto max-h-[500px]'):
                    ui.table.from_pandas(app.storage.tab['uploaded_file'], pagination={"rowsPerPage": 50}).classes('w-full text-sm text-black').props('dense')


    # Render Loading Spinner
    def render_spinner():

        spinner_container.clear()

        with spinner_container:
            with ui.column().classes('items-center justify-center gap-4') as spinner_div:
                ui.spinner('dots', color='black').classes('mt-4 text-6xl')

    
    # Render Process MQL

    #### UI BODY ###
    with ui.element('div').style('height: 90vh;').classes('flex pt-[20vh] justify-center max-w-[800px] w-full mx-auto'):
        with ui.column().classes('items-center w-full gap-4'):

            # Title
            ui.label('MQL AUTOMATION') \
                .style('font-size: 1.5rem;') \
                .classes('text-white font-poppins text-6xl normal-case text-center font-bold bg-black p-[0.5rem] rounded-lg mb-2')

            # Upload Area
            with ui.column().classes('items-center justify-center gap-4') as file_upload_div:
                with ui.row():
                    upload_component = ui.upload(
                        on_upload=excel_handler,
                        on_rejected=lambda: ui.notify('Rejected!'),
                        max_file_size=1_000_000_000,
                        max_files=1,
                        auto_upload=True
                    ).props('label="Browse" color=white text-color=black hide-upload-button accept=.xlsx') \
                    .classes('max-w-full rounded px-4 py-2')

            # Spinner and Work Containers
            spinner_container = ui.column()
            work_container = ui.column()




# Local deploymnet
#ui.run(port=8085, host='0.0.0.0', title='Seniority Classification', reload=False)

# Railway deploymnet
ui.run(
    host='0.0.0.0',
    port=int(os.getenv('PORT', 8080)),  # use Railway's port, fallback to 8080 locally
    title='MQL Automation',
    reload=False
)
