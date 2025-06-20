from nicegui import ui, events, app, run
import os
import re
from datetime import date

# layout
import opportunity_generator.layout.custom_html as ch
import opportunity_generator.layout.header as header

# function
import opportunity_generator.function as func

from starlette.formparsers import MultiPartParser
MultiPartParser.spool_max_size = 1024 * 1024 * 512  # 512 MB

@ui.page('/opportunity_generator')
async def main_app():


    try:
        await ui.context.client.connected(timeout=60.0) # <<< this line is critical
    except TimeoutError:
        print("Client connection timed out during page render. The browser took too long to connect.")
        ui.notify("Connection failed. Please refresh the page.", type='negative')
        return


    # --- Initialize app.storage.tab variables directly after connection ---
    if 'opp_generator_file' not in app.storage.tab:
        app.storage.tab['opp_generator_file'] = None 
    if 'excel_sheets_dict' not in app.storage.tab:
        app.storage.tab['excel_sheets_dict'] = {}
    if 'process_button' not in app.storage.tab:
        app.storage.tab['process_button'] = True
    if 'url_input' not in app.storage.tab:
        app.storage.tab['url_input'] = None
    if 'today_str' not in app.storage.tab:
        app.storage.tab['today_str'] = date.today().strftime('%Y-%m-%d')
    

    # Add Custom HTML
    ch.custom_html()

    # Header
    header.header()


    # UPLOAD AND READ EXCEL
    async def excel_upload_handler(event: events.UploadEventArguments):
        
        try:
            file_upload_div.visible = False # if file has been successfully upload - the upload button set to hidden

            render_spinner()

            content = event.content.read()  # Read bytes

            # Do Excel processing outside the handler
            app.storage.tab['excel_sheets_dict'] = await run.io_bound(func.read_excel_sheets, content)

            app.storage.tab['opp_generator_file'] = app.storage.tab['excel_sheets_dict'].get("Opportunity Generator")
            
            spinner_container.clear()
            
            if len(app.storage.tab['excel_sheets_dict']) > 0:
            
                print(len(app.storage.tab['excel_sheets_dict']))
                print(f"📦 excel_sheets_dict after load: {list(app.storage.tab['excel_sheets_dict'].keys())}")

                # process the file here
                func.start_process_opportunity()

                # export the file
                func.export_mql_work(app.storage.tab['opp_generator_file'], app.storage.tab['today_str'])
                ui.notify('Exported!')

            
            else:
                ui.notify('Error!')

            spinner_container.clear()
            upload_component.reset() # reset upload file component
            file_upload_div.visible = True 


        except:
            
            spinner_container.clear()
            upload_component.reset() # reset upload file component
            file_upload_div.visible = True # if file has been successfully upload - the upload button set to hidden

            ui.notify('Error!')
            

    
    # DOWNLOAD AND READ EXCEL
    async def excel_download_handler(input_url):

        try:

            ui.notify('Downloading File..')

            file_upload_div.visible = False # if file has been successfully upload - the upload button set to hidden
            render_spinner()
            content = await run.io_bound(func.download_excel, input_url)
            

            ui.notify('Reading File..')

            app.storage.tab['excel_sheets_dict'] = await run.io_bound(func.read_excel_sheets, content)
            app.storage.tab['opp_generator_file'] = app.storage.tab['excel_sheets_dict'].get("Opportunity Generator")


            spinner_container.clear()

            if len(app.storage.tab['excel_sheets_dict']) > 0:
            
                print(len(app.storage.tab['excel_sheets_dict']))
                print(f"📦 excel_sheets_dict after load: {list(app.storage.tab['excel_sheets_dict'].keys())}")

                # process the file here
                func.start_process_opportunity()

                # export the file
                func.export_mql_work(app.storage.tab['opp_generator_file'], app.storage.tab['today_str'])
                ui.notify('Exported!')


            
            else:
                ui.notify('Error!')

            spinner_container.clear()
            upload_component.reset() # reset upload file component
            file_upload_div.visible = True 



        except:
            spinner_container.clear()
            upload_component.reset() # reset upload file component
            file_upload_div.visible = True 

            ui.notify('Error!')


    ############## END READ EXCEL #################


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
            ui.label('OPPORTUNITY GENERATOR') \
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

