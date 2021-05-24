# -*- coding: utf-8 -*-
"""
@author:
    Verma, Himanshu
"""

import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from covidplasma_bot.input import paths

#----------------------------------------#
# credentials to the google account
def ghsheet_cred():
    # define the scope
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    
    cred = ServiceAccountCredentials.from_json_keyfile_name(paths.gsheet_json_file, scope)

    return cred

#----------------------------------------#
# getting google sheet data
def get_data_gsheet(sheet_client, sheet_name, sheet_index):
    
    # get the instance of the Spreadsheet
    sheet = sheet_client.open(sheet_name)
    
    # get the sheet_index sheet of the Spreadsheet
    sheet_instance = sheet.get_worksheet(sheet_index)

    # get all the records of the data
    records_data = sheet_instance.get_all_records()
    
    # convert the json to dataframe
    records_data = pd.DataFrame.from_dict(records_data)
    
    return records_data

#----------------------------------------#
# function for cleaning requester name
def fix_requester(requester):
    if requester.find(' ')==-1 and len(requester)>1:
        requester = requester.replace('@','')
        requester = '@' + requester
    elif len(requester)==0:
        requester = 'TSI form'
    elif len(requester)>20:
        requester = requester.split()[0]
    return requester

#----------------------------------------#
# function for removing special char from a string
def remove_special_char(string):
    string = ''.join(e for e in str(string) if e.isalnum())
    return string

#----------------------------------------#
# function for creating unique row_id of data
def create_row_id(data_df):
    row_id = ''
    for col in data_df.columns:
        if col not in ['','posted','row_id','Timestamp']:
            x = data_df[col].apply(lambda x: remove_special_char(x))
            x = x.apply(lambda x: str(x)[0:2]+str(x)[-2:])
            row_id = row_id + x
            
    return row_id