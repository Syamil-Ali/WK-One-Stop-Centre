import pandas as pd
from repos.opportunity_generator.action import opp_gen as opp

# PROCESS MQL


def start_opp_gen_pipeline(df, opp_file, acc_file, user_file):

    df_gen = pd.merge(df, acc_file[['CE Account Number','Id']], on='CE Account Number', how='left')

    df_gen = opp.opp_generator(df_gen, opp_file, user_file, "UpToDate")
    df_gen = opp.opp_generator(df_gen, opp_file, user_file, "Lexicomp")
    df_gen = opp.opp_generator(df_gen, opp_file, user_file, "Medispan")
    df_gen = opp.opp_generator(df_gen, opp_file, user_file, "EMMI")

    # drop column
    #df_gen.drop(columns='CE Account Number',inplace=True)


    return df_gen

