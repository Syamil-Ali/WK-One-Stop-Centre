from nicegui import ui, events, app, run
import os
from datetime import date

# layout
import pdf_to_table.layout.custom_html as ch
import pdf_to_table.layout.header as header

# function
import pdf_to_table.function as func

from starlette.formparsers import MultiPartParser
MultiPartParser.spool_max_size = 1024 * 1024 * 512  # 512 MB

@ui.page('/pdf_to_table')
async def main_app():


    try:
        await ui.context.client.connected(timeout=60.0) # <<< this line is critical
    except TimeoutError:
        print("Client connection timed out during page render. The browser took too long to connect.")
        ui.notify("Connection failed. Please refresh the page.", type='negative')
        return


    # --- Initialize app.storage.tab variables directly after connection ---
    if 'pdf_df_file' not in app.storage.tab:
        app.storage.tab['pdf_df_file'] = None 
    if 'today_str' not in app.storage.tab:
        app.storage.tab['today_str'] = date.today().strftime('%Y-%m-%d')
    

    # Add Custom HTML
    ch.custom_html()

    # Header
    header.header()


    # UPLOAD AND READ PDF
    async def pdf_upload_handler(event: events.UploadEventArguments):
        
        try:
            file_upload_div.visible = False # if file has been successfully upload - the upload button set to hidden

            render_spinner()

            content = event.content.read()  # Read bytes

            # Do Excel processing outside the handler
            app.storage.tab['pdf_df_file'] = await run.io_bound(func.read_pdf_and_export, content)

            spinner_container.clear()

            func.export_work(app.storage.tab['pdf_df_file'], app.storage.tab['today_str'])

            ui.notify('Exported!')

        except:

            ui.notify('Error!')
    
        spinner_container.clear()
        upload_component.reset() # reset upload file component
        file_upload_div.visible = True # if file has been successfully upload - the upload button set to hidden


    ############## END READ EXCEL #################


    # Render Loading Spinner
    def render_spinner():

        spinner_container.clear()

        with spinner_container:
            with ui.column().classes('items-center justify-center gap-4') as spinner_div:
                ui.spinner('dots', color='black').classes('mt-4 text-6xl')
       

    # Render Process MQL

    #### UI BODY ###
    with ui.element('div').style('height: 80vh;').classes('flex pt-[20vh] justify-center max-w-[800px] w-full mx-auto'):
        with ui.column().classes('items-center w-full gap-4'):

            # Title
            ui.label('PDF TO TABLE') \
                .style('font-size: 1.5rem;') \
                .classes('text-white font-poppins text-6xl normal-case text-center font-bold bg-black p-[0.5rem] rounded-lg mb-2')

            # Upload Area
            with ui.column().classes('items-center justify-center gap-4') as file_upload_div:
                with ui.row().classes('w-full max-w-[400px]'):
                    upload_component = ui.upload(
                        on_upload=pdf_upload_handler,
                        on_rejected=lambda: ui.notify('Rejected!'),
                        max_file_size=1_000_000_000,
                        max_files=1,
                        auto_upload=True
                    ).props('label="Upload" color=white text-color=black hide-upload-button accept=.pdf') \
                    .classes('max-w-full rounded px-4 py-2')
                

            # Spinner and Work Containers
            spinner_container = ui.column()

# Railway deploymnet
ui.run(
    host='0.0.0.0',
    port=int(os.getenv('PORT', 8080)),  # use Railway's port, fallback to 8080 locally
    title='WK One Stop Centre',
    reload=True
)

