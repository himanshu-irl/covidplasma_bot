# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 19:29:00 2021

@author: rajat
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe,get_as_dataframe

# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name("team-sos-tweet-f6228f19c798.json", scope)

# authorize the clientsheet 
client = gspread.authorize(creds)

# get the instance of the Spreadsheet
sheet = client.open('COVIDNews')

# get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(0)

existing = get_as_dataframe(sheet_instance,skip_blank_lines=True,header=0)

existing = existing[['Link', 'Title', 'Date', 'Topic', 'Label']]
existing = existing.dropna()

selected_news = existing.query('Label == 1').sample(n=1,random_state=1)

existing.loc[
    existing.query('Label == 1').sample(n=1,random_state=1).index,
    'Label'
] = 2

print(selected_news)
set_with_dataframe(sheet_instance, existing)