import pandas as pd


# get the routing file
# read targetted sales team file

GOV_SALES_REP = "Justin Schenker"

def cleanup_sales_rep(route_file, route_file_territory): # df_provider_postal, df_provider_territories

    # clean up the postal code file first
    route_file.columns = route_file.columns.str.strip()
    route_file['Postal Code'] = route_file['Postal Code'].astype(str).str.zfill(5)




    # to get the associated sales person
    route_file_territory.columns = route_file_territory.columns.str.strip()



    #---------------------------- TO CLEAN SALES TEAM DF -----------------------#

    region_name_store = ['WEST', 'MIDWEST', 'MIDATLANTIC', 'SOUTHEASTPRO', 'NORTHEASTPRO', 'CANADA, NATIONAL ACCOUNTS', 'GOVERNMENT', 'Drug Information Sales Specialists & EMR Account and Relationship Executive']

    df_copy = route_file_territory.copy()

    # Assuming df is your DataFrame and the column of interest is called 'Column_Name'
    indices_with_region = df_copy[df_copy['US PROVIDER REGION & TERRITORY ASSIGNMENTS'].str.contains('Region:', na=False)].index

    # Convert to list if you need a list of indices
    indices_with_region_list = indices_with_region.tolist()

    store_df = []

    # create a multiple df
    for index, value in enumerate(indices_with_region_list):
        
        # get the last index value
        try:
            last_index_value = indices_with_region_list[index+1]
        except:
            last_index_value = 0.99
            
        if last_index_value != 0.99:
            region_df = df_copy.iloc[value:last_index_value]
        else: 
            region_df = df_copy.iloc[value::]
            
        store_df.append(region_df)



    region_df_dict = {}


    for df in store_df:
        
        # 1 -------- get the region 
        region = df['US PROVIDER REGION & TERRITORY ASSIGNMENTS'].iloc[0].replace('Region:','').strip()
        print(region)

        # rename southeast pro region only
        if region == "SOUTHEAST PRO":
            region = 'SOUTHEASTPRO'
        
        # 2 ------- cleanup the df
        
        copy_df = df.copy()

        # Extract the second row (index 1) and ignore the rows above it
        # Step 1: Set the second row as the column names

        copy_df.columns = copy_df.iloc[1]

        # Step 2: Drop all rows above the new column names row, including that row itself
        copy_df = copy_df.iloc[2::]
        copy_df = copy_df.dropna(how='all')
        copy_df = copy_df.dropna(axis=1, how='all')
        
        # need to handle government and the rest
        if (region == 'Government') or  (region == 'Drug Information Sales Specialists & EMR Account and Relationship Executive'):
            #print('true')
            copy_df.columns.values[0] = 'Territory Name'
            
        
        #try:
        fill_in_col = list(copy_df.columns)
        fill_in_col.remove('Territory Name')

        copy_df[fill_in_col] = copy_df[fill_in_col].ffill()
        
        # drop rows that has missing value in the first column
        copy_df = copy_df.dropna(subset=['Territory Name'])
        
        region_df_dict[region] = copy_df


    # PRINT KEY
    return route_file, region_df_dict

#---------------------------- TO CLEAN SALES TEAM DF (END) -----------------------#




# ------------------ TO GET THE SALES TEAM --------------------- #


# start doing
def get_sales_team(region, territory, product, region_df_dict, status='New Business'):
    
    # ----------
    # status here - new business rep / renewal (or existing)
    # ----------

    try:
        if (region == 'please check') or (territory == 'please check'):
            return 'please check'

        # to handle lexi, medispan, emmi -- will improve this in the future
        if status != 'Renewal':
            status = 'New Business'
        
        # get the region
        region_df = region_df_dict[region].copy()
        
        if region == 'WEST':
            region_df.rename(columns={'Drug Information Sales Specialist':'Lexi New Business Rep'}, inplace=True)

        # fix for any weird
        region_df['Territory Name'] = region_df['Territory Name'].str.replace('\xa0', ' ').str.strip()

        # need to clean the value Territory Name value
        region_df['Territory Name'] = region_df['Territory Name'].str.replace(r'\(.*?\)', '', regex=True).str.strip()
        
        #  then grab the by the product
        if product == 'UpToDate':
            

            sales_rep = region_df[region_df['Territory Name'] == territory]['Inside Team'].iloc[0]
            #return sales_rep, region_df[region_df['Territory Name'] == territory]

            
        elif (product == 'Medi-Span') or (product == 'Lexicomp'):
            
            sales_rep_full = region_df[region_df['Territory Name'] == territory]['Lexi New Business Rep'].iloc[0]
            
            if status == 'New Business':
                sales_rep_list = sales_rep_full.split('\n')
                
                sales_rep = sales_rep_list[1].replace('Inside rep:','')
                sales_rep = sales_rep.strip()
                
            elif status == 'Renewal':
                sales_rep_list = sales_rep_full.split('\n')
                
                sales_rep = sales_rep_list[0].replace('Field rep:','')
                sales_rep = sales_rep.strip()
            
            else:
                sales_rep = 'please check'
                
            # in here has inside team and field rep - i think can do when has prev sales team - then use the existing one
            
        elif product == 'Emmi':
            
            # check for status
            if status == 'New Business':
                sales_rep = region_df[region_df['Territory Name'] == territory]['Emmi Sales Executive for Patient Engagement (New Business)'].iloc[0]
                
                
            elif status == 'Renewal':
                sales_rep = region_df[region_df['Territory Name'] == territory]['Emmi Sales Executive for Patient Engagement (Renewal Business)'].iloc[0]
                
            else:
                sales_rep = 'please check'
                
                
        
        else:
            sales_rep = 'please check'
            
        
    
        return sales_rep
    except:
        return 'got error'



# FOR GOVERNMENT, CANADA, NATIONAL ACCOUNTS
def get_sales_team_else(region, territory, product, region_df_dict, status='New Business'):

    if region.upper() == 'GOVERNMENT':

        region_df = region_df_dict['Government'].copy()


        if (product == 'Medi-Span') or (product == 'Lexicomp'):

            territory = "Government Account Manager"
            
            sales_rep_full = region_df[region_df['Territory Name'] == territory]['Lexi New Business Rep'].iloc[0]
            
            if status == 'New Business':
                sales_rep_list = sales_rep_full.split('\n')
                
                sales_rep = sales_rep_list[1].replace('Inside rep:','')
                sales_rep = sales_rep.strip()
                
            elif status == 'Renewal':
                sales_rep_list = sales_rep_full.split('\n')
                
                sales_rep = sales_rep_list[0].replace('Field rep:','')
                sales_rep = sales_rep.strip()
            
            else:
                sales_rep = 'please check'

        else:
            sales_rep = ' or '.join(region_df_dict['Government']['Directors'].tolist())
    

    elif region == "CANADA, NATIONAL ACCOUNTS": 

        region_df = region_df_dict['CANADA, NATIONAL ACCOUNTS'].copy()

        # HANDLE Territory for National Accounts
        if territory == 'NA1':
            territory = 'NATIONAL ACCOUNTS (NA1)'
        elif territory == 'NA2':
            territory = 'NATIONAL ACCOUNTS (NA2)'
        elif territory == 'NA3':
            territory = 'NATIONAL ACCOUNTS (NA3)'
    

        if (product == 'Medi-Span') or (product == 'Lexicomp'):

            sales_rep_full = region_df[region_df['Territory Name'] == territory]['Lexi New Business Rep'].iloc[0]
            
            if status == 'New Business':
                sales_rep_list = sales_rep_full.split('\n')
                
                sales_rep = sales_rep_list[1].replace('Inside rep:','')
                sales_rep = sales_rep.strip()
                
            elif status == 'Renewal':
                sales_rep_list = sales_rep_full.split('\n')
                
                sales_rep = sales_rep_list[0].replace('Field rep:','')
                sales_rep = sales_rep.strip()
            
            else:
                sales_rep = 'please check'

        else:
            sales_rep = region_df[region_df['Territory Name'] == territory]['Director'].iloc[0]


    return sales_rep







# ------------------ TO GET THE SALES TEAM (END) --------------------- #




# ------------------ TO GET THE REGION AND TERRITORY BASED ON THE ZIPCODE --------------------- #

def location_finder(route_file, zipcode):


    try:

        zipcode = str(zipcode).zfill(5)

        region = route_file[route_file['Postal Code'] == zipcode]['Sales Region Name'].iloc[0]
        territory = route_file[route_file['Postal Code'] == zipcode]['2025 Territory'].iloc[0]


    except:
        region = 'please check'
        territory = 'please check'


    # start finding th sales rep


    return region, territory



# ------------------ MAIN FUNCTION WORK --------------------- #
def main_sales_rep(region_df_dict, df_provider_postal, row):

    # get the region
    # Check for NaN and convert safely
    if pd.isna(row['ZipCode']) or row['ZipCode'] == "":
        region, territory = 'Got error', 'Got error'  # Assign default values if NaN

    # check for the canada
    elif str(row['ZipCode']).upper() == "EASTERN - WESTERN CANADA":
        region = "CANADA, NATIONAL ACCOUNTS"
        territory = "EASTERN - WESTERN CANADA"
        sales_rep = get_sales_team_else(region, territory, row['PRODUCT'], region_df_dict, status='New Business')
        return territory, "CANADA", sales_rep
    
    elif str(row['ZipCode']).upper()  == "ONTARIO":
        region = "CANADA, NATIONAL ACCOUNTS"
        territory = "ONTARIO"
        sales_rep = get_sales_team_else(region, territory, row['PRODUCT'], region_df_dict, status='New Business')
        return territory, "CANADA", sales_rep
    
    elif str(row['ZipCode']).upper()  == "NA1":
        region = "CANADA, NATIONAL ACCOUNTS"
        territory = "NA1"
        sales_rep = get_sales_team_else(region, territory, row['PRODUCT'], region_df_dict, status='New Business')
        return territory, "NATIONAL ACCOUNTS", sales_rep
    
    elif str(row['ZipCode']).upper()  == "NA2":
        region = "CANADA, NATIONAL ACCOUNTS"
        territory = "NA2"
        sales_rep = get_sales_team_else(region, territory, row['PRODUCT'], region_df_dict, status='New Business')
        return territory, "NATIONAL ACCOUNTS", sales_rep
    
    elif str(row['ZipCode']).upper()  == "NA3":
        region = "CANADA, NATIONAL ACCOUNTS"
        territory = "NA3"
        sales_rep = get_sales_team_else(region, territory, row['PRODUCT'], region_df_dict, status='New Business')
        return territory, "NATIONAL ACCOUNTS", sales_rep

    elif str(row['ZipCode']).upper()  == "GOVERNMENT":
        region = "GOVERNMENT"
        territory = ""
        sales_rep = get_sales_team_else(region, territory, row['PRODUCT'], region_df_dict, status='New Business')
        return territory, "GOVERNMENT", sales_rep
        

    else:
        region, territory = location_finder(df_provider_postal, str(int(row['ZipCode'])))

    # get the sales team
    sales_rep = get_sales_team(region, territory, row['PRODUCT'], region_df_dict, status='New Business')

    return territory, region, sales_rep
    