import pandas as pd

# 1. GET THE TERRITORY, REGION FROM MDM ID
# [input] - account object, mdm_id
# [output] - territory, region
def get_location_mdm_id(mdm_id, account_object):

    try:

        # convert the type of mdm_id
        mdm_id = str(mdm_id)

        # filter the df object with the mdm id
        acc_info = account_object[account_object['MDM Id'] == mdm_id].copy()

        # get the territory and region
        print(acc_info['WK CE Territory'])
        territory = acc_info['WK CE Territory'].iloc[0]
        region = acc_info['Sales Region'].iloc[0]

        # return
        return territory, region

    except Exception as e:
        print(f'Error: {e}')
        return 'error', 'error'
    


def get_location_zipcode(zipcode, wk_territory, total_item, product):

    # rules:
    utd_growth = 203
    utd_key = 760

    lexi_growth = 615
    lexi_key = 2300

    '''
    UPTODATE

    Any unassigned MQL up to 203 providers will go to the Growth tier
    Any unassigned MQL from 204 to 760 will go to the Key tier
    Any unassigned MQL over 761 providers will trigger an email to Matt, Don, and Ron McBride (this should be very rare)
    

    LEXIDRUG

    Any unassigned MQL up to 615 beds will go to the Growth tier
    Any unassigned MQL from 616 beds to 2,300 beds will go to the Key tier
    Any unassigned MQL over 2,301 beds will trigger an email to Matt, Don, and Ron McBride (this should be very rare)
    

    MEDI-SPAN – Use the same logic as Lexidrug for now

    

    PATIENT ENGAGEMENT – We are getting more information on how to route these MQLs
    
    '''


    try:
        
        # convert to str
        zipcode = str(zipcode)
        acc_info = wk_territory[wk_territory['Postal Code'] == zipcode].copy()


        if product.strip().upper() == 'UPTODATE':

            if total_item <= utd_growth:

                territory = acc_info['2025 GROWTH'].iloc[0] # for UTD
                region = territory[:-2]

            elif total_item <= utd_key:

                territory = acc_info['2025 KEY'].iloc[0] # for UTD
                region = territory[:-2]


        # lexicomp, medi-span 
        elif (product.strip().upper() == 'LEXICOMP') or (product.strip().upper() == 'MEDI-SPAN'):

            if total_item <= lexi_growth:

                territory = acc_info['2025 GROWTH'].iloc[0] # for UTD
                region = territory[:-2]

            elif total_item <= lexi_key:

                territory = acc_info['2025 KEY'].iloc[0] # for UTD
                region = territory[:-2]

        else:
            territory = 'KIV'
            region = 'KIV'
    
        return territory, region


    except Exception as e:
        print(f'Error: {e}')
        return 'error', 'error'



# get the sales rep (by default, we will be using the new sales rep)
def get_sales_rep(product, wk_new_assignment, territory):

    try:
        assignment_info = wk_new_assignment[
            wk_new_assignment['WK CE Territory'].str.strip().str.upper() == territory.strip().upper()
        ].copy()

        acc_owner = assignment_info['Account Owner'].iloc[0]

        if product.strip().upper() == 'UPTODATE':
            sales_rep = assignment_info['UTD New Business Manager'].iloc[0]
            

        elif (product.strip().upper() == 'LEXICOMP') or (product.strip().upper() == 'MEDI-SPAN'):
            sales_rep = assignment_info['Lexi / Medi New Business Manager'].iloc[0]

        elif product.strip().upper() == 'EMMI':
            sales_rep = assignment_info['Patient Engagement Manager'].iloc[0]

        else:
            sales_rep = 'Error'

        return sales_rep, acc_owner
    
    except Exception as e:
        print(f'Error: {e}')
        return 'error', 'error'
    

def number_type(item_count):
    try:
        if item_count is None:
            return 0
        return int(str(item_count).strip())
    except ValueError:
        return 0


def main_sales_rep(row, account_object, wk_territory, wk_new_assignment):


    # check if the mdm exist or
    try:
        print(row['MDM ID'])
        int(row['MDM ID'].strip()) # to check if mdm id is valid or not

        # if valid, get the territory and region
        territory, region = get_location_mdm_id(row['MDM ID'].strip(), account_object)

    except: # if mdm not exist

        try:
            if str(row['PRODUCT']).strip().upper() == 'UPTODATE':

                # get the value
                value = number_type(row['Number Clinicians'])

                territory, region = get_location_zipcode(row['ZipCode'], wk_territory, value, row['PRODUCT'])

            elif (str(row['PRODUCT']).strip().upper() == 'LEXICOMP') or (str(row['PRODUCT']).strip().upper() == 'MEDI-SPAN'):
            
                # get the value
                value = number_type(row['Total Beds'])

                territory, region = get_location_zipcode(row['ZipCode'], wk_territory, value, row['PRODUCT'])

            else:
                return 'error', 'error', 'error', 'error'
            
        except Exception as e:
            print(e)
            return 'error', 'error', 'error', 'error'
        
    
    # get the sales rep
    sales_rep, acc_owner = get_sales_rep(row['PRODUCT'], wk_new_assignment, territory)

    return territory, region, sales_rep, acc_owner