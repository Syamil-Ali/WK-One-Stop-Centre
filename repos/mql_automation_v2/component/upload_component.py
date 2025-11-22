from nicegui import ui, events, app, run

import requests
import polars as pl
import pandas as pd
import io


from repos.mql_automation_v2.component.table_component import render_mql_work_table
from repos.mql_automation_v2.component.spinner_component import render_spinner, unrender_spinner



main_file = 'Work Task'
sheet_names = sheet_names = [main_file, 'Account Object', 'Opportunity Object', 'User Object', 'WK - Provider National Account', 'WK - New Territory', 'WK - New Assignment']

# READ EXCEL FILE
def read_excel_sheets(content, sheet_names = sheet_names):

    result_dict = {}

    try:
        for sheet in sheet_names:
            try:
                with io.BytesIO(content) as f:
                        df = pl.read_excel(f, sheet_name=sheet).to_pandas()
                        if not df.empty:
                            df = df.dropna(how="all")
                            result_dict[sheet] = df
                            print(f'✅ Loaded sheet: {sheet}, {len(df)} rows')
                        else:
                            print(f'⚠️ Sheet "{sheet}" is empty or not found')
                            break
            except Exception as e:
                print(f'❌ Failed to read sheet: {sheet} → {e}')
                return {}
    
        return result_dict
    
    except Exception as e:
        ui.notify(f'Failed to parse Excel: {e}')
        print(e)



with ui.dialog() as loading_dialog, ui.card():
    ui.label("Uploading... Please wait")
    ui.spinner(size="lg")


async def handle_upload(e):
    
    # save the filename
    try:

        #loading_dialog.open() 

        render_spinner()
        app.storage.tab['file_name'] = e.name
        print("UPLOAD CALLED!")  # <-- to confirm the handler runs


        content = e.content.read()

        app.storage.tab['excel_sheets_dict'] = await run.io_bound(read_excel_sheets, content)
        app.storage.tab['main_file'] = app.storage.tab['excel_sheets_dict'].get(main_file)

        print('pass')
        unrender_spinner()

        ui.notify(f"Uploaded: {e.name}, rows: {len(app.storage.tab['main_file'])}")

        # trigger the table rendering component
        render_mql_work_table()

    except Exception as e:
        ui.notify(f"Error: Missing Sheets or Wrong File")
        unrender_spinner()
        app.storage.tab['main_body'].visible = True
        app.storage.tab['upload_component'].reset() # reset upload file component
        app.storage.tab['table_container'].clear()



def pro_upload(
    label: str = "Click or drag .xlsx here",
    accept: str = ".xlsx",
    max_files: int = 1,
    max_file_size: int = 1_000_000_000,
    on_upload=None,
):
    # Visual dropzone card
    with ui.card().classes(
        'w-full max-w-xl mx-auto rounded-2xl border-2 border-line '
        'border-blue-400 bg-blue-50 shadow-sm transition hover:shadow-md '
        'p-10 flex flex-col items-center justify-center space-y-3'
    ).style('position: relative; overflow: hidden; cursor: pointer;') as card:

        ui.icon('cloud_upload').classes(
            'text-6xl text-blue-500 transition-all duration-300'
        )
        ui.label(label).classes(
            'text-lg font-medium text-blue-700 transition-colors duration-300'
        )
        ui.label(f'Allowed: .xlsx • Max 100 MB').classes(
            'text-sm text-blue-400'
        )

        # Add spinner (hidden initially)
        # floating spinner overlay (hidden by default)
        spinner_overlay = ui.column().style(
            'position: absolute; left: 0; top: 0; right: 0; bottom: 0; '
            'display: none; '
            'align-items: center; justify-content: center; '
            'background: rgba(255,255,255,0.78); backdrop-filter: blur(4px); '
            'z-index: 50; padding: 0; margin: 0;' 
            'pointer-events: none;')
        with spinner_overlay:
            ui.spinner(size='lg', color='blue')

        # Transparent uploader
        uploader = ui.upload(
            on_upload=handle_upload,
            on_rejected=lambda: ui.notify('File rejected'),
            max_file_size=max_file_size,
            max_files=max_files,
            auto_upload=True,
        ).props(f'hide-upload-button accept={accept}')

        uploader.style(
            'position: absolute; inset: 0; width: 100%; height: 100%; '
            'opacity: 0; z-index: 2; cursor: pointer;'
        )

        # Show spinner when uploading starts
        uploader.on('added', lambda e: spinner_overlay.style('display: flex;'))
        # Hide spinner when finished
        uploader.on('uploaded', lambda e: spinner_overlay.style('display: none;'))

        # Clicking anywhere on the card should open the file dialog
        uploader.on('click', lambda e: uploader.run_method('pickFiles'))

        # Dragging feedback
        card.on('dragover', lambda e: card.classes(add='bg-blue-50 border-blue-500'))
        card.on('dragleave', lambda e: card.classes(remove='bg-blue-50 border-blue-500'))
        card.on('drop', lambda e: card.classes(remove='bg-blue-50 border-blue-500'))

    return uploader



# DOWNLOAD EXCEL FILE
def download_excel(url):

    if 'download=1' not in url:
        if '?' in url:
            url += '&download=1'
        else:
            url += '?download=1'


    resp = requests.get(url, allow_redirects=True)

    if resp.status_code == 200:
        return resp.content
    else:
        print(f'❌ Failed to Download sheet')


# DOWNLOAD AND READ EXCEL
async def excel_download_handler(input_url):

    try:

        ui.notify('Downloading File..')

        render_spinner()
        content = await run.io_bound(download_excel, input_url)
        app.storage.tab['file_name'] = 'Download MQL'
        ui.notify('Reading File..')

        app.storage.tab['excel_sheets_dict'] = await run.io_bound(read_excel_sheets, content)
        app.storage.tab['main_file'] = app.storage.tab['excel_sheets_dict'].get(main_file)
        unrender_spinner()

        if len(app.storage.tab['excel_sheets_dict']) > 0:
        
            print(len(app.storage.tab['excel_sheets_dict']))
            print(f"📦 excel_sheets_dict after load: {list(app.storage.tab['excel_sheets_dict'].keys())}")

            render_mql_work_table()
        
        else:
            app.storage.tab['main_body'].visible = True # if file has been successfully upload - the upload button set to hidden
            unrender_spinner()
            ui.notify('Error!')

    except:
        app.storage.tab['main_body'].visible = True # if file has been successfully upload - the upload button set to hidden
        unrender_spinner()

        ui.notify('Error!')
