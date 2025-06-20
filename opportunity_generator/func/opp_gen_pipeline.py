import pandas as pd
from opportunity_generator.func import opp_gen as opp
from opportunity_generator import function as func


def start_opp_gen_pipeline(df, content, opp_file_name, acc_file_name, user_file_name):


    # Account file
    # read account file
    acc_file = func.read_excel_sheet_mini(content, acc_file_name) # read the acc_file
    print('pass acc file')

    df_gen = pd.merge(df, acc_file[['CE_Account_Number__c','Id']], left_on='CE-Account Number', right_on='CE_Account_Number__c', how='left')

    acc_file = None # to clear the memory after use


    # read for the rest
    opp_file = func.read_excel_sheet_mini(content, opp_file_name) # read the acc_file
    print('pass opp file')
    
    user_file = func.read_excel_sheet_mini(content, user_file_name) # read the acc_file
    print('read user file')

    # Main File, Opp file, User File
    df_gen = opp.opp_generator(df_gen, opp_file, user_file, "UpToDate")
    df_gen = opp.opp_generator(df_gen, opp_file, user_file, "Lexicomp")
    df_gen = opp.opp_generator(df_gen, opp_file, user_file, "Medispan")
    df_gen = opp.opp_generator(df_gen, opp_file, user_file, "EMMI")

    # clear file
    opp_file = None
    user_file = None
    print('pass generate')


    # drop column
    df_gen.drop(columns='CE_Account_Number__c',inplace=True)


    return df_gen

