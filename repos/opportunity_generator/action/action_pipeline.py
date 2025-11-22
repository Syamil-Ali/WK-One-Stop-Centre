import pandas as pd
from repos.opportunity_generator.action import opp_gen as opp
import numpy as np

# PROCESS MQL


def start_opp_gen_pipeline(df, opp_file, acc_file, user_file):

    df_gen = pd.merge(df, acc_file[['CE Account Number','Id', 
                                    'UpToDate Customer Status', 'Lexicomp Customer Status', 'Medi Span Customer Status','Emmi Customer Status']], on='CE Account Number', how='left')

    df_gen = opp.opp_generator(df_gen, opp_file, user_file, "UpToDate")
    df_gen = opp.opp_generator(df_gen, opp_file, user_file, "Lexicomp")
    df_gen = opp.opp_generator(df_gen, opp_file, user_file, "Medispan")
    df_gen = opp.opp_generator(df_gen, opp_file, user_file, "EMMI")

    # add confidence

    # Condition: (Status is 'active') AND (Product is NOT missing) 1 Value if True (both conditions met), else 0
    df_gen['UpToDate Confidence'] = np.where(
        # Condition: (Status is 'active') AND (Product is NOT missing)
        (df_gen['UpToDate Customer Status'].str.lower() == 'active') & (df_gen['UpToDate - Product'].notna()) |
        (df_gen['UpToDate Customer Status'].str.lower() != 'active') & (df_gen['UpToDate - Product'].isna())
        ,1,0)

    df_gen['Lexicomp Confidence'] = np.where(
        # Condition: (Status is 'active') AND (Product is NOT missing)
        (df_gen['Lexicomp Customer Status'].str.lower() == 'active') & (df_gen['Lexicomp - Product'].notna()) |
        (df_gen['Lexicomp Customer Status'].str.lower() != 'active') & (df_gen['Lexicomp - Product'].isna())
        ,1,0)

    df_gen['Medi-Span Confidence'] = np.where(
        # Condition: (Status is 'active') AND (Product is NOT missing)
        (df_gen['Medi Span Customer Status'].str.lower() == 'active') & (df_gen['Medispan - Product'].notna()) |
        (df_gen['Medi Span Customer Status'].str.lower() != 'active') & (df_gen['Medispan - Product'].isna())
        ,1,0)

    df_gen['Emmi Confidence'] = np.where(
        # Condition: (Status is 'active') AND (Product is NOT missing)
        (df_gen['Emmi Customer Status'].str.lower() == 'active') & (df_gen['EMMI - Product'].notna()) |
        (df_gen['Emmi Customer Status'].str.lower() != 'active') & (df_gen['EMMI - Product'].isna())
        ,1,0)
    
    # combine all
    df_gen['Final Confidence Score'] = (
        (df_gen['UpToDate Confidence'] + 
        df_gen['Lexicomp Confidence'] + 
        df_gen['Medi-Span Confidence'] + 
        df_gen['Emmi Confidence']) / 4 
    ) * 100

    df_gen = df_gen.drop(columns = ['UpToDate Confidence', 'Lexicomp Confidence','Medi-Span Confidence','Emmi Confidence'])

    return df_gen
