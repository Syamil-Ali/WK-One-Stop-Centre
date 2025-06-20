import polars as pl
import pandas as pd
import io
from nicegui import ui, app
import tempfile
from opportunity_generator.func import opp_gen_pipeline as og
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
def read_excel_sheets(content): # Predefined Opportunity Generator Tab

    sheet_names = ['Opportunity Generator', 'Opportunity Object', 'User Object', 'Account Object']
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




# EXPORT MQL WORK FILE
def export_mql_work(uploaded_file, today_date):
    
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
            uploaded_file.to_csv(tmp.name, index=False)
            tmp.flush()
            ui.download(tmp.name, filename=f'result-opportunity-{str(today_date)}.csv')
    else:
        ui.notify('No file to download')


# PROCESS MQL
def start_process_opportunity():


    # predefined the item
    df_opp = app.storage.tab['excel_sheets_dict']['Opportunity Object']
    df_acc= app.storage.tab['excel_sheets_dict']['Account Object']
    df_opp_owner= app.storage.tab['excel_sheets_dict']['User Object']

    app.storage.tab['opp_generator_file'] = og.start_opp_gen_pipeline(app.storage.tab['opp_generator_file'], df_opp, df_acc, df_opp_owner)
