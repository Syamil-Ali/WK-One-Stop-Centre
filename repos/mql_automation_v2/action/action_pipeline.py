import pandas as pd
import polars as pl
from repos.mql_automation_v2.action import sales_rep as sr
from repos.mql_automation_v2.action import opp_func as of
from repos.mql_automation_v2.action import comment_generated as cg


def main_pipeline(df_work, df_opp, df_opp_owner,  df_provider_new_territories, df_provider_new_assignment, df_acc):


    ############### 1 ###############
    # To clean up the Postal Code and Sales Rep and Opp File
    #df_provider_postal, region_df_dict = sr.cleanup_sales_rep(df_provider_postal, df_provider_territories)
    df_opp_combined = of.opp_combine(df_opp, df_opp_owner)
    print('PASS 1: CLEAN UP FILE')


    ############### 2 ###############
    # Generate opp comments
    print('📄 Columns in df_work:', df_work.columns.tolist())
    df_work['Opportunity Comment'] = df_work['Salesforce Account ID'].apply(lambda x: of.opp_main_work(df_opp_combined, x))

    print('PASS 2: GENERATE OPP')


    ############### 3 ###############
    # Generate Regions, Territories, Sales Rep
    #df_work[['Territory', 'Region', 'Sales Rep']] = df_work.apply(lambda x: sr.main_sales_rep(region_df_dict, df_provider_postal, x), axis=1, result_type="expand")
    df_work[['Territory', 'Region', 'Sales Rep', 'Account Owner',
             'Territory Template', 'Region Template', 'Sales Rep Template', 'Account Owner Template',
             ]] = df_work.apply(lambda x: sr.main_sales_rep(x, df_acc, df_provider_new_territories, df_provider_new_assignment), axis=1, result_type="expand")

    
    print('PASS 3: GENERATE SALES REP')

    ############### 4 ###############
    # Generate Comment
    df_work['Comment'] = df_work.apply(lambda x: cg.populate_comment_general(x), axis=1)
    print('PASS 4: GENERATE COMMENT')


    ############### 5 ###############
    # Reorder Column
    df_work = df_work[['DATE RECEIVED','YEAR','MONTH','COMPANY', 'LEAD NAME','LEAD TITLE','LEAD EMAIL',
                        'SOURCE: TACTIC', 'SOURCE: CAMPAIGN', 'PRODUCT', 'Territory', 'Region', 'Sales Rep', 'Comment', 'Account Owner',
                        'Lead: Segment', 'Organization Type', 'Salesforce Account Segment',
                        'Comment City', 'Comment State', 'Comment Zipcode', 'Salesforce Territory','Salesforce Region',
                        'Territory Template', 'Region Template', 'Sales Rep Template', 'Account Owner Template'
                        ]]
    print('PASS 5: REORDERED COLUMNS')


    return df_work

