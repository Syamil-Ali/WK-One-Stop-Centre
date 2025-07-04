from nicegui import ui, events, app, run
import os
import re
from datetime import date

# layout
#import mql_automation.layout.custom_html as ch
#import mql_automation.layout.header as header
import layout.header as header
import layout.custom_html as ch

# function
from mql_automation import function as func
from starlette.formparsers import MultiPartParser
MultiPartParser.spool_max_size = 1024 * 1024 * 512  # 512 MB



@ui.page('/mql_automation')
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
    if 'process_button' not in app.storage.tab:
        app.storage.tab['process_button'] = True
    if 'url_input' not in app.storage.tab:
        app.storage.tab['url_input'] = None
    if 'today_str' not in app.storage.tab:
        app.storage.tab['today_str'] = date.today().strftime('%Y-%m-%d')
    

    # Add Custom HTML
    ch.custom_html()

    # Header
    current_path = ui.context.client.request.url.path
    header.header(current_path)


    # UPLOAD AND READ EXCEL
    async def excel_upload_handler(event: events.UploadEventArguments):
        
        try:
            file_upload_div.visible = False # if file has been successfully upload - the upload button set to hidden
            
            app.storage.tab['file_name'] = event.name

            render_spinner()

            content = event.content.read()  # Read bytes

            # Do Excel processing outside the handler
            app.storage.tab['excel_sheets_dict'] = await run.io_bound(func.read_excel_sheets, content)

            app.storage.tab['uploaded_file'] = app.storage.tab['excel_sheets_dict'].get("Work Task")
            
            spinner_container.clear()
            
            if len(app.storage.tab['excel_sheets_dict']) > 0:
            
                print(len(app.storage.tab['excel_sheets_dict']))
                print(f"📦 excel_sheets_dict after load: {list(app.storage.tab['excel_sheets_dict'].keys())}")

                render_mql_work_table()
            
            else:
                file_upload_div.visible = True # if file has been successfully upload - the upload button set to hidden
                spinner_container.clear()
                upload_component.reset() # reset upload file component

                ui.notify('Error!')

        except:
            file_upload_div.visible = True # if file has been successfully upload - the upload button set to hidden
            spinner_container.clear()
            upload_component.reset() # reset upload file component

            ui.notify('Error!')
            

    
    # DOWNLOAD AND READ EXCEL
    async def excel_download_handler(input_url):

        try:

            ui.notify('Downloading File..')

            file_upload_div.visible = False # if file has been successfully upload - the upload button set to hidden
            render_spinner()
            content = await run.io_bound(func.download_excel, input_url)
            app.storage.tab['file_name'] = 'Download MQL'
            ui.notify('Reading File..')

            app.storage.tab['excel_sheets_dict'] = await run.io_bound(func.read_excel_sheets, content)
            app.storage.tab['uploaded_file'] = app.storage.tab['excel_sheets_dict'].get("Work Task")
            spinner_container.clear()

            if len(app.storage.tab['excel_sheets_dict']) > 0:
            
                print(len(app.storage.tab['excel_sheets_dict']))
                print(f"📦 excel_sheets_dict after load: {list(app.storage.tab['excel_sheets_dict'].keys())}")

                render_mql_work_table()
            
            else:
                file_upload_div.visible = True # if file has been successfully upload - the upload button set to hidden
                spinner_container.clear()
                ui.notify('Error!')



        except:
            file_upload_div.visible = True # if file has been successfully upload - the upload button set to hidden
            spinner_container.clear()
            ui.notify('Error!')





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
                        app.storage.tab['process_button'] = ui.button('Process', 
                                                   on_click= lambda: func.start_process_mql(work_container, render_spinner, spinner_container, render_mql_work_table)
                                                   ).props('flat rounded').classes('text-black font-poppins font-medium normal-case')
                        #process_button.visible = True
                        ui.button('Export', on_click= lambda: func.export_mql_work(app.storage.tab['uploaded_file'], app.storage.tab['today_str'])).props('flat rounded').classes('text-black font-poppins font-medium normal-case')
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

    
    # Render Submit Button
    def submit_button_url():

        submit_url_button_container.clear()

        with submit_url_button_container:
            ui.button('Pull Data', on_click= lambda: excel_download_handler(app.storage.tab['url_input'].value)).props('flat rounded').classes(
                    'font-poppins font-medium normal-case  button-bordered hover:text-white'
                )


    # function validation url
    def is_valid_url(url: str) -> bool:
        # Basic URL validation regex (you can customize further)
        regex = re.compile(
            r'^(https?|ftp)://'  # protocol
            r'[\w\-]+(\.[\w\-]+)+[/#?]?.*$',  # domain and path
            re.IGNORECASE,
        )
        return re.match(regex, url) is not None

    def validate_url(e):
        if is_valid_url(e.value):
            app.storage.tab['url_input'].classes(remove='border-red-500')
            app.storage.tab['url_input'].classes('border-green-500')
            submit_button_url()
            
        else:
            app.storage.tab['url_input'].classes(remove='border-green-500')
            app.storage.tab['url_input'].classes('border-red-500')
            submit_url_button_container.clear()


            

    # Render Process MQL

    #### UI BODY ###
    with ui.element('div').style('height: 80vh;').classes('flex pt-[20vh] justify-center max-w-[800px] w-full mx-auto'):
        with ui.column().classes('items-center w-full gap-4'):

            # Title
            ui.label('MQL AUTOMATION') \
                .style('font-size: 1.5rem;') \
                .classes('text-white font-poppins text-6xl normal-case text-center font-bold bg-black p-[0.5rem] rounded-lg mb-2')

            # Upload Area
            with ui.column().classes('items-center justify-center gap-4') as file_upload_div:
                with ui.row().classes('w-full max-w-[400px]'):
                    upload_component = ui.upload(
                        on_upload=excel_upload_handler,
                        on_rejected=lambda: ui.notify('Rejected!'),
                        max_file_size=1_000_000_000,
                        max_files=1,
                        auto_upload=True
                    ).props('label="Upload" color=white text-color=black hide-upload-button accept=.xlsx') \
                    .classes('max-w-full rounded px-4 py-2')

                # URL INPUT
                ui.label('----- or -----').classes('font-poppins font-bold')

                with ui.row().classes('w-full max-w-[400px]'):
                    app.storage.tab['url_input'] = ui.input(
                        label='Excel URL',
                        on_change=validate_url
                    ).props('input-class="pb-4"'
                    ).classes(
                        'h-[55px] bg-white rounded-full border-2 text-black font-poppins px-4 w-[100%]'
                    )
                
                submit_url_button_container = ui.column()
                




            # Spinner and Work Containers
            spinner_container = ui.column()
            work_container = ui.column()

