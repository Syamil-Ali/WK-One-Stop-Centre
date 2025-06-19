import polars as pl
import pandas as pd
import io
from nicegui import ui, app
import tempfile
from mql_automation.func import main_pipeline as mp
import requests

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
        


# READ EXCEL FILE
def read_excel_sheets(content):

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
                return {}
    
        return result_dict
    
    except Exception as e:
        ui.notify(f'Failed to parse Excel: {e}')
        print(e)


# DELETE MQL WORK FILE
def delete_mql_work(upload_component, file_upload_div, work_container):

    app.storage.tab['excel_sheets_dict'] = {} 
    app.storage.tab['uploaded_file'] = None
    app.storage.tab['file_name'] = None
    app.storage.tab['process_button'] = True

    upload_component.reset() # reset upload file component
    file_upload_div.visible = True # make the upload div appear back after remove the file
    work_container.clear()  # Clear the UI rendering
    ui.notify('File deleted')  # Optional notification


# EXPORT MQL WORK FILE
def export_mql_work(uploaded_file, today_date):
    
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
            uploaded_file.to_csv(tmp.name, index=False)
            tmp.flush()
            ui.download(tmp.name, filename=f'result-mql-{str(today_date)}.csv')
    else:
        ui.notify('No file to download')


# PROCESS MQL
def start_process_mql(work_container, render_spinner, spinner_container, render_mql_work_table):


    work_container.clear()  # Remove old content if any

    # predefined the item
    df_opp = app.storage.tab['excel_sheets_dict']['Opportunity Object']
    df_opp_owner= app.storage.tab['excel_sheets_dict']['User Object']
    df_national_acc = app.storage.tab['excel_sheets_dict']['WK - Provider National Account']
    df_provider_territories = app.storage.tab['excel_sheets_dict']['WK - Provider Territories']
    df_provider_postal = app.storage.tab['excel_sheets_dict']['WK - Provider Postal Code Data']

    render_spinner()

    app.storage.tab['uploaded_file'] = mp.main_pipeline(app.storage.tab['uploaded_file'], df_opp, df_opp_owner, df_national_acc, df_provider_territories, df_provider_postal)

    spinner_container.clear()
    render_mql_work_table()
    ui.notify('DONE!', type='positive', position='top')
    app.storage.tab['process_button'].visible = False