import pandas as pd
import polars as pl


def opp_combine(df_opp, df_opp_owner):

# full code

    # drop duplicates
    df_opp_owner.drop_duplicates(inplace=True)

    # Merge on 'ID' column (inner join by default)
    merged_df = df_opp.merge(df_opp_owner, on='OwnerId', how='inner')
    merged_df.shape

    return merged_df


def product_identifier(data):
    
    product = []
    
    try:
        if 'UpToDate' in data['Subsidiary']:
            product.append('UpToDate')
        if 'Lexicomp' in data['Subsidiary']:
            product.append('Lexicomp')
        if 'Emmi' in data['Subsidiary']:
            product.append('Emmi')
        if 'Medi-Span' in data['Subsidiary']:
            product.append('Medi-Span')
    except:
        pass
    
    
    # 2nd way
    if len(product) == 0:
        if data['Lexicomp Sub-Total'] > 0: 
            product.append('Lexicomp')

        if data['UpToDate Sub-Total'] > 0:
            product.append('UpToDate')

        if data['Medi-Span Sub-Total'] > 0:
            product.append('Medi-Span')

        if data['Emmi Sub-Total'] > 0:
            product.append('Emmi')
        
        
    # 3rd ways
    if len(product) == 0:
        
        # check within opp name
        if 'lexicomp' in data['Opportunity Name'].lower():
            product.append('Lexicomp')
        if 'lexi' in data['Opportunity Name'].lower():
            product.append('Lexicomp')
        if 'rx' in data['Opportunity Name'].lower():
            product.append('Medi-Span')
        if 'medispan' in data['Opportunity Name'].lower():
            product.append('Medi-Span')
        if 'emmi' in data['Opportunity Name'].lower():
            product.append('Emmi')
        if 'uptodate' in data['Opportunity Name'].lower():
            product.append('UpToDate')
        if 'utd' in data['Opportunity Name'].lower():
            product.append('UpToDate')
        if 'up-to-date' in data['Opportunity Name'].lower():
            product.append('UpToDate')
            
    
    product = list(set(product)) # remove duplicate
    # can do check subsidiary also
        
    return ';'.join(product)



def create_comment(item):
    
    opp_url = f"https://wkce.lightning.force.com/lightning/r/Opportunity/{item['Opportunity ID']}/view"
    
    if item['Stage'] == 'Closed Lost':
        text = f"- They had {item['item_finalized']} closed lost in {item['Close Date'].strftime('%b/%Y')}. The link is here: {opp_url}"
        
    else:
        if item['Type'] == 'New':
            text = f"- They have {item['item_finalized']} {item['Stage'][:2]} opportunity. The link is here: {opp_url}"
            
        else:
            text = f"- They are {item['item_finalized']} active customer with {item['Stage'][:2]} opportunity. The link is here: {opp_url}"
            
    
    return text


# MAIN FUNCTION
def opp_main_work(merged_df, acc_id):

    # merged both opp file
    # merged_df = opp_combine(df_opp, df_opp_owner) # i think this one will be the main function instead

    # filter based on the acc
    try:
        df = merged_df[merged_df['AccountId'] == acc_id].copy()
        df.dropna(subset=['Close Date'], inplace=True) #drop missing


        # start check source opp
        source_opportunity = [x for x in df['Source Opportunity'] if pd.notna(x)]


        # add a new column that shows renewal or not - the idea is that to remove any unnecessary opp here
        df['renewal status'] = df['Opportunity Name'].apply(lambda x: 'True' if x in source_opportunity else 'False')

        # provide the product of the opportunity
        df['item_finalized'] = df.apply(lambda x:product_identifier(x), axis=1)

        # select only the distinct
        df_copy = df[df['renewal status'] == 'False'].copy()
        df_copy['Close Date'] = pd.to_datetime(df_copy['Close Date']) # convert to datetime
        df_copy['Created Date'] = pd.to_datetime(df_copy['Created Date']) # convert to datetime

        # sort by close date (desc)
        df_copy = df_copy.sort_values(by=['Close Date'], ascending=False)

        # tick for the first occurence
        df_copy['first_occurrence'] = df_copy['item_finalized'].duplicated(keep='first').apply(lambda x: 0 if x else 1)

        # copy the first occurence only
        new_df_copy = df_copy[df_copy['first_occurrence'] == 1].copy()

        # generate the comment for the opp
        new_df_copy['Comment Generated'] = new_df_copy.apply(lambda x: create_comment(x), axis=1)

        # convert to list
        comment_list = new_df_copy['Comment Generated'].tolist()
        comment_string = '\n'.join(f"{item}" for item in comment_list)

        return comment_string
    
    except:
        return ''