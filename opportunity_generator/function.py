import polars as pl
import pandas as pd
import io
from nicegui import ui, app
import tempfile
from opportunity_generator.func import opp_gen_pipeline as og
import requests
import openpyxl

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
        


# CHECK SHEET
def check_excel_sheets(content):

    sheet_names = ['Opportunity Generator', 'Opportunity Object', 'User Object', 'Account Object']


    try:
        # Load the workbook in read-only mode, which is very memory efficient.
        # It reads only the structure and not the cell data.
        workbook = openpyxl.load_workbook(io.BytesIO(content), read_only=True, data_only=False)
        
        # Get the actual sheet names from the loaded workbook
        actual_sheet_names = workbook.sheetnames
        
        # Close the workbook immediately to free resources
        workbook.close()
        
        # Check if all required sheets are present
        for sheet_name in sheet_names:
            if sheet_name not in actual_sheet_names:
                print(f"Sheet '{sheet_name}' not found in the Excel file.")
                return [] # Or raise an error, or return False
        
        # If all required sheets are found, return the list of required sheet names
        print(f"All required sheets found: {sheet_names}")
        return sheet_names
    
    except Exception as e:
        # This will catch errors during workbook loading (e.g., corrupted file)
        print(f'❌ Failed to parse Excel file for sheet check: {e}')
        return [] # Or False, as per your original logic
    


# To Read One File
def read_excel_sheet_mini(content, sheet_name):

    try:
        with io.BytesIO(content) as f:
            df = pl.read_excel(f, sheet_name=sheet_name).to_pandas()
            if not df.empty:
                return df
            else:
                print(f'⚠️ Sheet "{sheet_name}" is empty or not found')

        return None
    except Exception as e:
        print(f'❌ Failed to read sheet: {sheet_name} → {e}')
        return None
        







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
def start_process_opportunity(work_df, content):


    # predefined the item
    df_opp = 'Opportunity Object' #app.storage.tab['excel_sheets_dict']['Opportunity Object']
    df_acc= 'Account Object' #app.storage.tab['excel_sheets_dict']['Account Object']
    df_opp_owner= 'User Object' #app.storage.tab['excel_sheets_dict']['User Object']

    work_df = og.start_opp_gen_pipeline(work_df, content, df_opp, df_acc, df_opp_owner)

    return work_df
