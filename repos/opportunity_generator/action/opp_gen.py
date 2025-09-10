import pandas as pd
import polars as pl


product_mix_column = 'Product Mix'

def opp_generator(df, opp_file, user_file, opp_type):

    # opp_type
    # 1. UpToDate
    # 2. Lexicomp
    # 3. Medi-Span
    # 4. Emmi

    #print(opp_file.columns)

    try:
        if opp_type == 'UpToDate':
            column_sub_total = 'UpToDate Sub-Total'
        if opp_type == 'Lexicomp':
            column_sub_total = 'Lexicomp Sub-Total'
        if opp_type == 'Medispan':
            column_sub_total = 'Medi-Span Sub-Total'
        if opp_type == 'EMMI':
            column_sub_total = 'Emmi Sub-Total'
            
        
        opp_filter = opp_file[(opp_file[product_mix_column] == opp_type) | (opp_file[product_mix_column] == 'Combo')].copy()
    
        
        
        # drop s1, s7 and closed lost
        opp_filter = opp_filter[
            (opp_filter['Stage'] != 'Closed Lost') &
            (opp_filter['Stage'] != 'S7 Order Finalized') &
            (opp_filter['Stage'] != 'S1 Account Development')]
        
        
        opp_filter = opp_filter[
            ~((opp_filter[product_mix_column] == "Combo") &
            (opp_filter[column_sub_total] <= 0))]
    
        
        # to filter based on the id
        opp_filter = opp_filter[opp_filter['AccountId'].isin(df['Id'])].copy()
        
        # drop date na
        opp_filter.dropna(subset=['Close Date'], inplace=True)
        
        # identify the 
        # Identify source opportunities (for renewal checking)
        source_opps = opp_filter['Source Opportunity'].dropna().tolist()
        
        # Mark older renewals based on source opportunities
        opp_filter['renewal status'] = opp_filter['Opportunity Name'].apply(
            lambda x: 'True' if x in source_opps else 'False'
        )
        
        # remove out older opp
        opp_filter = opp_filter[opp_filter['renewal status'] == 'False'].copy()
        
        # sort by close date
        opp_filter.sort_values(by='Close Date', ascending=False, inplace=True)
        
        # drop duplicates
        opp_filter.drop_duplicates(subset='AccountId', inplace=True)
    
        # generate product column
        opp_filter['Product'] = opp_type


        print(opp_filter.columns)
    
        # select important column
        opp_filter_new = opp_filter[['AccountId', 'Product', 'Type','Close Date', 'Annual Contract Value', 'Opportunity ID', 'Product Mix', 'OwnerId', 'Opportunity Number']]
    
    
        # Rename column
        col_rename = {
            "Type": f'{opp_type} - Type',
            "Close Date": f'{opp_type} - Close Date',
            "Opportunity ID": f'{opp_type} - Opportunity ID',
            "Annual Contract Value": f'{opp_type} - ACV',
            "Product": f"{opp_type} - Product",
            "AccountId": "Id",
            "Product Mix": f"{opp_type} - Product Mix",
            "OwnerId": f"{opp_type} - OwnerId",
            "Opportunity Number": f"{opp_type} - Opp Num"
        }
        
        opp_filter_new = opp_filter_new.copy()
        opp_filter_new.rename(columns=col_rename, inplace=True)
        #print(opp_filter_new.shape)
    
        # merge
        df_merge = pd.merge(df, opp_filter_new, on = "Id", how="left")

        df_gen_w_opp = pd.merge(df_merge, user_file, left_on=f"{opp_type} - OwnerId", right_on='OwnerId', how='left')

        df_gen_w_opp.drop(columns=[f"{opp_type} - OwnerId", 'OwnerId'], inplace=True)

        df_gen_w_opp.rename(columns={'Owner Name': f"{opp_type} - Owner Name"}, inplace=True)

        return df_gen_w_opp

    except Exception as e:
        print(e)
        df[
            [
                f"{opp_type} - Product",
                f"{opp_type} - Type",
                f"{opp_type} - Close Date",
                f"{opp_type} - ACV",
                f"{opp_type} - Opportunity ID"
            ]
        ] = ''

        return df

            
        
    


