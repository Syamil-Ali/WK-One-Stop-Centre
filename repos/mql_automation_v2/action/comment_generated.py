import pandas as pd
import polars as pl
import datetime



def populate_comment_general(row): # data here is row


    # check if it is sfdc info or not
    date_comment = datetime.datetime.now().date().strftime('%m/%d/%Y') # get the date


    try:
        # check total bed
        total_bed = int(row['Total Beds'])
        if total_bed != 0:
            beds_comment = f"{row['Salesforce Account Classification'] if (pd.notna(row['Salesforce Account Classification']) and (row['Salesforce Account Classification'] != '')) else row['Organization Type']} with {total_bed} beds"
        else:
            beds_comment = f"{row['Salesforce Account Classification'] if (pd.notna(row['Salesforce Account Classification']) and (row['Salesforce Account Classification'] != '')) else row['Organization Type']}"
    except:
        total_bed = 0
        beds_comment = f"{row['Salesforce Account Classification'] if (pd.notna(row['Salesforce Account Classification']) and (row['Salesforce Account Classification'] != '')) else row['Organization Type']}"


    # physician comment
    try:
        # check total bed
        total_provider = int(row['Number Clinicians'])
        if total_provider != 0 and total_bed != 0:
            provider_comment = f"and {total_provider} providers"
        elif total_provider != 0 and total_bed == 0:
            provider_comment = f"with {total_provider} providers"
        else:
            provider_comment = f""
    except:
        provider_comment = f""




    
    try:
        int(row['MDM ID'])

        account_status = f"- According to SFDC this is an {beds_comment} {provider_comment}. They are headquartered in {row['HQ Address']}. Their website is here: {row['Web URL']}".strip()
        account_url_comment = f"- This is an existing account in Salesforce. The link is here {row['Salesforce Account URL']}".strip()
        
    except:
        account_status = f"- This is an {beds_comment} {provider_comment}. They are headquartered in {row['HQ Address']}. Their website is here: {row['Web URL']}".strip()
        account_url_comment = f"- This is not an existing account in Salesforce.".strip()
        
# need to add hq address
    # time to generate comment


    try:
        # LINKEDIN CHECK
        linkedin_comment = f"{'Their LinkedIn profile is here: ' + row['Lead LinkedIn URL'] if row['Lead LinkedIn URL'] else ''}"
    except:
        linkedin_comment = ''


    # assigned person
    raw_name = str(row['Assigned Person']).strip()
    name = raw_name.lower()
    
    if name == 'syamil ali':
        assigned_person = 'Syamil'
    elif name == 'syifa khairi':
        assigned_person = 'SK'
    elif 'carlota' in name or 'canopin' in name:
        assigned_person = 'Carlota'
    else:
        # Use first name if present
        assigned_person = raw_name.split()[0] if raw_name else ""
    

    #print(row['Assigned Person'])
    #print(assigned_person)


        
    comment_lines = [
        f"{date_comment} {assigned_person}:" ,
        f"- This is a lead for {row['PRODUCT']} that came in from a {row['SOURCE: TACTIC']}.",
        account_status,
        f"- The lead's title is {row['LEAD TITLE']}. {linkedin_comment}",
        account_url_comment if account_url_comment else '',
        f"{row['Opportunity Comment']}" if row['Opportunity Comment'] else '',  # Skips if empty
        f"- Based on headquarter location, this lead is located in the {row['Territory']} territory in the {row['Region']} region. It should be assigned to {row['Sales Rep']} and {row['Account Owner']}.",
    ]

    # Join non-empty lines to avoid blank lines
    comment = "\n".join(line for line in comment_lines if line.strip())
    

    return comment
