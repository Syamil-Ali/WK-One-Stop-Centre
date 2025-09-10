import polars as pl
import pandas as pd
import io
from nicegui import ui, app
import tempfile
import pdfplumber



# READ PDF FILE
def read_pdf_and_export(content): # Predefined Opportunity Generator Tab

    
    all_tables = []
    try:

        with pdfplumber.open(io.BytesIO(content)) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    df = pd.DataFrame(table)  # Treat all rows as data
                    all_tables.append(df)

    except Exception as e:
        print(f'ERROR: {e}')
    
    # combine all table
    # concat the tables
    combined_df = pd.concat(all_tables, ignore_index=True)
    
    return combined_df
