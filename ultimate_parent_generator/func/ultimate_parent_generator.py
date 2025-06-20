import pandas as pd



def get_ultimate_parent_ce_number(df_work, df_account):
    
    # get their ultimate parent mdm_id
    df_gen = pd.merge(df_work, df_account[['CE_Account_Number__c','Ultimate_Parent_Account_MDM_Id__c']], left_on='CE-Account Number', right_on='CE_Account_Number__c', how='left')
    print('pass gen 1')
    # and get the ce number back based on the ultimate
    df_gen = pd.merge(df_gen, df_account[['CE_Account_Number__c','MDM_Id__c', 'Sales_Region__c', 'WK_CE_Territory__c', 'Name','Classification__c','Id']], left_on='Ultimate_Parent_Account_MDM_Id__c', right_on='MDM_Id__c', how='left')
    print('pass gen 2')
    
    # drop column
    df_gen = df_gen[['CE-Account Number', 'CE_Account_Number__c_y', 'Name','Classification__c','Sales_Region__c','WK_CE_Territory__c', 'Id']]
    
    df_gen.rename(columns={
        'CE_Account_Number__c_y':'Ultimate Parent CE-Account Number',
        'Sales_Region__c'       :'Ultimate Parent Sales Region',
        'WK_CE_Territory__c'    :'Ultimate Parent Territory',
        'Name'                  :'Ultimate Parent Account Name',
        'Classification__c'     :'Ultimate Parent Classification',
        'Id'                    :'Ultimate Parent Account ID',
    }, inplace=True)

    print('pass gen 3')


    
    return df_gen
                  
