import pandas as pd



def get_ultimate_parent_ce_number(df_work, df_account):
    
    # get their ultimate parent mdm_id
    df_gen = pd.merge(df_work, df_account[['Name', 'MDM Id','CE Account Number','Ultimate Parent Account MDM Id']], on='CE Account Number', how='left')
    
    print('pass 1: get the ultimate parent mdm id')

    # and get the ce number back based on the ultimate
    df_gen = pd.merge(df_gen, df_account[['CE Account Number','MDM Id', 'Sales Region', 'WK CE Territory', 'Name','Classification','Id', 'Account Owner']], left_on='Ultimate Parent Account MDM Id', right_on='MDM Id', how='left')
    print('pass 2: get the info of the ultimate parent')
    
    # drop column
    #df_gen = df_gen.drop(columns=['MDM Id'])
    #df_gen = df_gen[['CE Account Number', 'Ultimate Parent Account MDM Id', 'CE Account Number_y','Name','Classification','Sales Region','WK CE Territory', 'Id']]
    
    df_gen.rename(columns={
        'Name_x'                :'Account Name',
        'CE Account Number_x'   :'CE Account Number',
        'MDM Id_x'              :'MDM Id',

        'Name_y'                :'Ultimate Parent Account Name',
        'CE Account Number_y'   :'Ultimate Parent CE Account Number',
        'Sales Region'          :'Ultimate Parent Sales Region',
        'WK CE Territory'       :'Ultimate Parent Territory',
        'Classification'        :'Ultimate Parent Classification',
        'Id'                    :'Ultimate Parent Account ID',
        'Account Owner'         :'Ultimate Parent Account Owner'
    }, inplace=True)

    print('pass gen 3: compile all info')


    # sort
    df_gen = df_gen[['CE Account Number', 'MDM Id','Account Name', 
                     'Ultimate Parent CE Account Number', 'Ultimate Parent Account MDM Id', 'Ultimate Parent Account Name','Ultimate Parent Classification',
                     'Ultimate Parent Territory','Ultimate Parent Sales Region','Ultimate Parent Account ID','Ultimate Parent Account Owner']]


    
    return df_gen
                  
