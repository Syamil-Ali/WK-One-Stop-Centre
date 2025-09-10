import polars as pl
import pandas as pd
from nicegui import ui, app
import tempfile
from datetime import date



# DELETE WORK FILE
def delete_file():

    # item manipulation
    app.storage.tab['excel_sheets_dict'] = {} 
    app.storage.tab['main_file'] = None
    app.storage.tab['file_name'] = None
    app.storage.tab['process_button'] = True

    # ui layout manipulation
    app.storage.tab['upload_component'].reset() # reset upload file component
    app.storage.tab['main_body'].visible = True # make the main body div appear back after remove the file
    app.storage.tab['table_container'].clear()  # Clear the UI rendering
    ui.notify('File deleted')  # Optional notification


# EXPORT WORK FILE
def export_file(file_type='other'):

    
    today_date = date.today().strftime('%Y-%m-%d')

    if file_type == 'mql':
        start_name = 'result-mql-'

    elif file_type == 'pdf':
        start_name = 'result-pdf-'

    elif file_type == 'ultimate_parent_generator':
        start_name = 'ultimate-parent-info'

    elif file_type == 'opportunity_generator':
        start_name = 'opportunity-info'
    else:
        start_name = ''


    if app.storage.tab['main_file'] is not None:
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
            app.storage.tab['main_file'].to_csv(tmp.name, index=False)
            tmp.flush()
            ui.download(tmp.name, filename=f'{start_name}-{str(today_date)}.csv')
    else:
        ui.notify('No file to download')
