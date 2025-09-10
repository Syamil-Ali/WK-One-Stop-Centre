# MAIN
from nicegui import ui, events, app, run
import os
from io import BytesIO
import pandas as pd

# LAYOUT
from layout.custom_html import custom_html
from layout.header import header

# COMPONENT
from .component.upload_component import pro_upload, handle_upload, excel_download_handler
from .component.table_component import render_mql_work_table

# UTILS
from utils.utils import is_valid_url

from starlette.formparsers import MultiPartParser
MultiPartParser.spool_max_size = 1024 * 1024 * 512  # 512 MB

#https://samanthadigital.com/blue-color-palette/

# UPLOAD AND READ EXCEL



# Render Submit Button
def submit_button_url():

    app.storage.tab['submit_button_container'].clear()

    with app.storage.tab['submit_button_container']:
        ui.button('Pull Data', on_click= lambda: excel_download_handler(app.storage.tab['url_input'].value)).props('flat rounded').classes(
                'font-poppins font-medium normal-case  button-bordered hover:text-white'
            )




def validate_url(e):
    if is_valid_url(e.value):
        app.storage.tab['url_input'].classes(remove='border-red-500')
        app.storage.tab['url_input'].classes('border-green-500')
        submit_button_url()
        
    else:
        app.storage.tab['url_input'].classes(remove='border-green-500')
        app.storage.tab['url_input'].classes('border-red-500')
        app.storage.tab['submit_button_container'].clear()


title = 'MQL Automation - v2'
description = 'Automates the process of compiling and generating lead notes.'

@ui.page('/mql_automation_v2')
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
    if 'main_file' not in app.storage.tab:
        app.storage.tab['main_file'] = None 
    if 'excel_sheets_dict' not in app.storage.tab:
        app.storage.tab['excel_sheets_dict'] = {} 
    if 'file_name' not in app.storage.tab:
        app.storage.tab['file_name'] = None 
    if 'process_button' not in app.storage.tab:
        app.storage.tab['process_button'] = True
    if 'url_input' not in app.storage.tab:
        app.storage.tab['url_input'] = None
    if 'table_container' not in app.storage.tab:
        app.storage.tab['table_container'] = None

    custom_html()

    current_path = ui.context.client.request.url.path
    header(ui.context.client.request.url.path)

    # MAIN COMPONENT DF
    with ui.element('div').style('height: 85vh;').classes('flex pt-[10vh] justify-center max-w-[800px] w-full mx-auto'):

        with ui.grid(columns='1fr 1fr').style('height: 450px;').classes('w-full gap-2') as app.storage.tab['main_body']:
            
            ####################### LEFT BLOCK #########################
            # DESCRIPTION SECTION
            with ui.column().classes('items-start justify-center'):
                # Title
                ui.label(title) \
                    .style('font-size: 1.5rem;') \
                    .classes('text-white font-poppins text-6xl normal-case text-center font-bold bg-black p-[0.5rem] rounded-lg mb-2')

                ui.label(description).classes('text-md font-poppins font-semibold')

            ####################### RIGHT BLOCK #########################
            # UPLOAD SECTION
            with ui.column().classes('items-center justify-center bg-[#4B97C9] px-2 rounded-2xl border-2 border-line border-[#1B4965]'):
                with ui.row().classes('w-full max-w-[400px]'):
                    # Example usage
                    app.storage.tab['upload_component'] = pro_upload()
                    

                # URL INPUT
                ui.label('----- or -----').classes('font-poppins font-bold')

                with ui.row().classes('w-full max-w-[400px]'):
                    app.storage.tab['url_input'] = ui.input(
                        label='Excel URL',
                        on_change=validate_url,
                    ).props('input-class="pb-4" Standout'
                    ).classes(
                        'h-[55px] bg-white rounded-md border-2 text-black font-poppins px-4 w-[100%]'
                    )
                
                app.storage.tab['submit_button_container'] = ui.column()

        # define the table component ui
        app.storage.tab['table_container'] = ui.column()

        # define the spinner component
        app.storage.tab['spinner_container'] = ui.column()
            
        

'''
ui.run(
    host='0.0.0.0',
    port=int(os.getenv('PORT', 8080)),  # use Railway's port, fallback to 8080 locally
    title='WK One Stop Centre',
    reload=True,
    reconnect_timeout=300
)
'''
