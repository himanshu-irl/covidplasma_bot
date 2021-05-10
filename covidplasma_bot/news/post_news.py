# -*- coding: utf-8 -*-
"""
Created on Fri May  7 20:30:53 2021

@author: rajat
"""
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe,get_as_dataframe
from datetime import datetime, timedelta
from covidplasma_bot.input import tweet_parameter as param
from covidplasma_bot.poster import tweet_poster as tpost
from covidplasma_bot.input import paths
import pandas as pd

gsheet_json_file = paths.gsheet_json_file
news_post_template = param.news_post_template

def get_news_from_gsheets():
    # define the scope
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    
    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name(gsheet_json_file, scope)
    
    # authorize the clientsheet 
    client = gspread.authorize(creds)
    
    # get the instance of the Spreadsheet
    sheet = client.open('COVIDNews')
    
    # get the first sheet of the Spreadsheet
    sheet_instance = sheet.get_worksheet(0)
    
    existing = get_as_dataframe(sheet_instance)
    news_df = existing[['Link', 'Title', 'Date','Topic', 'Label']].dropna()
    news = news_df[(news_df['Label'] == 1) & (pd.to_datetime(news_df['Date']).astype('datetime64[ns]') > datetime.utcnow() - timedelta(hours=2))].sample(n=1)
    #news = news_df[['Link', 'Title', 'Date','Topic', 'Label']]
    #updated = news.append(existing)
    #print(news['Date'].str[17:25] > (datetime.utcnow() - timedelta(hours=2)).strftime("%H:%M:%S") )
    #print(datetime.utcnow().strftime("%H:%M:%S"))
    #print(news['Date'])
    news_df['Label'][news.index.tolist()[0]] = 2
    set_with_dataframe(sheet_instance, news_df)
    news = news.reset_index(drop=True)
    return news

def news_post(CONSUMER_KEY
            ,CONSUMER_SECRET
            ,ACCESS_KEY
            ,ACCESS_SECRET
            ,tgram_token
            ,tgram_success_chatid
            ,logger
            ,data):
    
    # extracting news title and link
    news_title = data['Title'][0]
    news_link = data['Link'][0]

    # creating news tweet template
    template = param.news_post_template
    template = template.replace('::title::',news_title)
    template = template.replace('::link::',news_link)

    try:
        tpost.post_tweet(CONSUMER_KEY
                        ,CONSUMER_SECRET
                        ,ACCESS_KEY
                        ,ACCESS_SECRET
                        ,tgram_token
                        ,tgram_success_chatid
                        ,logger
                        ,input_txt=template)
    
    except:
        print('error encountered...')