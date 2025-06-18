import pandas as pd
import polars as pl
from func import sales_rep as sr
from func import opp_func as of
from func import comment_generated as cg


# pass to pandas for now
#df_work = df_work.to_pandas()
#df_opp = df_opp.to_pandas()
#df_opp_owner = df_opp_owner.to_pandas()
#df_national_acc = df_national_acc.to_pandas()
#df_provider_territories = df_provider_territories.to_pandas()
#df_provider_postal = df_provider_postal.to_pandas()



def main_pipeline(df_work, df_opp, df_opp_owner, df_national_acc, df_provider_territories, df_provider_postal):

    # columns handler
    #columns_default = ['DATE RECEIVED','YEAR','MONTH','COMPANY','LEAD NAME','LEAD TITLE','LEAD EMAIL','SOURCE: TACTIC','SOURCE: CAMPAIGN','PRODUCT','MDM ID','Total Beds','Current Customer','Number Clinicians','HQ Address','ZipCode','Lead LinkedIn URL','Web URL','COMMENTS / NOTES','Organization Type','Comment Street','Comment City','Comment State','Comment Zipcode','Assigned Person','Lead: Segment','Status','Lead: Lead ID','Marketo Sales Insight','Lead Marketo Sales Insight URL','Contacts Marketo Sales Insight URL','MDM ID Lead','MDM ID Account','Salesforce Account ID','Salesforce Account Classification','Salesforce National Account','Salesforce Account Segment','Salesforce Territory','Salesforce Region','Salesforce Total Beds','Salesforce Account URL']
    # Find missing columns
    #columns_left = [col for col in columns_default if col not in df_work.columns]

    # Add missing columns with empty string values
    #df_work[columns_left] = ''


    ############### 1 ###############
    # To clean up the Postal Code and Sales Rep and Opp File
    df_provider_postal, region_df_dict = sr.cleanup_sales_rep(df_provider_postal, df_provider_territories)
    df_opp_combined = of.opp_combine(df_opp, df_opp_owner)
    print('PASS 1: CLEAN UP FILE')


    ############### 2 ###############
    # Generate opp comments
    print('📄 Columns in df_work:', df_work.columns.tolist())
    df_work['Opportunity Comment'] = df_work['Salesforce Account ID'].apply(lambda x: of.opp_main_work(df_opp_combined, x))

    print('PASS 2: GENERATE OPP')


    ############### 3 ###############
    # Generate Regions, Territories, Sales Rep
    df_work[['Territory', 'Region', 'Sales Rep']] = df_work.apply(lambda x: sr.main_sales_rep(region_df_dict, df_provider_postal, x), axis=1, result_type="expand")
    print('PASS 3: GENERATE SALES REP')

    ############### 4 ###############
    # Generate Comment
    df_work['Comment'] = df_work.apply(lambda x: cg.populate_comment_general(x), axis=1)
    print('PASS 4: GENERATE COMMENT')


    ############### 5 ###############
    # Reorder Column
    df_work = df_work[['DATE RECEIVED','YEAR','MONTH','COMPANY', 'LEAD NAME','LEAD TITLE','LEAD EMAIL',
                        'SOURCE: TACTIC', 'SOURCE: CAMPAIGN', 'PRODUCT', 'Territory', 'Region', 'Sales Rep', 'Comment',
                        'Lead: Segment', 'Organization Type', 'Salesforce National Account', 'Salesforce Account Segment',
                        'Comment City', 'Comment State', 'Comment Zipcode', 'Salesforce Territory','Salesforce Region']]
    print('PASS 5: REORDERED COLUMNS')


    return df_work

