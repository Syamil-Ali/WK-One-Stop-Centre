import pandas as pd
from opportunity_generator.func import opp_gen as opp


def start_opp_gen_pipeline(df, opp_file, acc_file, user_file):

    df_gen = pd.merge(df, acc_file[['CE_Account_Number__c','Id']], left_on='CE-Account Number', right_on='CE_Account_Number__c', how='left')

    df_gen = opp.opp_generator(df_gen, opp_file, user_file, "UpToDate")
    df_gen = opp.opp_generator(df_gen, opp_file, user_file, "Lexicomp")
    df_gen = opp.opp_generator(df_gen, opp_file, user_file, "Medispan")
    df_gen = opp.opp_generator(df_gen, opp_file, user_file, "EMMI")

    # drop column
    df_gen.drop(columns='CE_Account_Number__c',inplace=True)


    return df_gen

