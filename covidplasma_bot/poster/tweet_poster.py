# -*- coding: utf-8 -*-
"""
@author:
    Verma, Himanshu
"""

import tweepy
from covidplasma_bot.helper import telegram_poster as tp
import gspread
import pandas as pd
from gspread_dataframe import set_with_dataframe
from datetime import datetime, timedelta
import time
import random
import pytz
from covidplasma_bot.helper import tweet_handler as th
from covidplasma_bot.helper import gsheet_handler as gh
from covidplasma_bot.poster import img_creator as ic

def post_tweet(CONSUMER_KEY
            ,CONSUMER_SECRET
            ,ACCESS_KEY
            ,ACCESS_SECRET
            ,tgram_token
            ,tgram_success_chatid
            ,logger
            ,input_txt):

    try:
        # authenticating twitter account
        print('authenticating connection...')
        logger.info('authenticating connection...')
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

        # posting on twitter
        print('publishing post on twitter...')
        logger.info('publishing post on twitter...')
        api.update_status(input_txt)
        # sending log to telegram
        tp.send_message(tgram_token
                            ,tgram_success_chatid
                            ,'Tweet POST - CovidPlasmaIn - ' + str(input_txt))
    except:
        print('error encountered in posting...')

# function for posting resources
def resource_poster(sheet_name
                    ,cred
                    ,tsi_api
                    ,copla_api
                    ,tgram_token
                    ,tgram_success_chatid
                    ,logger
                    ,image_path
                    ,output_path
                    ,font_path
                    ,rand_sleep
                    ,sleep_lag):

    # authorize the clientsheet 
    print('authenticating connection...')
    logger.info('authenticating connection...')
    client = gspread.authorize(cred)

    # getting prod and aux sheet data
    print('getting sheet data...')
    logger.info('getting sheet data...')
    prod_data = gh.get_data_gsheet(client, sheet_name, 0)
    aux_data = gh.get_data_gsheet(client, sheet_name, 1)

    # filtering latest data (getting requests from last 24 hours)
    print('filtering sheet data...')
    logger.info('filtering sheet data...')
    current_time = datetime.now(pytz.timezone('Asia/Calcutta')).replace(tzinfo=None)
    prod_data = prod_data[pd.to_datetime(prod_data['Timestamp'], format='%d/%m/%Y %H:%M:%S') > current_time - timedelta(hours=12)]

    # creating row_id for joining pord and aux sheets
    print('creating row_id for sheet data...')
    logger.info('creating row_id for sheet data...')
    prod_data['row_id'] = gh.create_row_id(prod_data)
    aux_data['row_id'] = gh.create_row_id(aux_data)

    # left joing aux to prod data
    print('joining both sheets data...')
    logger.info('joining both sheets data...')
    prod_aux_data = pd.merge(prod_data, aux_data, how="left", on=['row_id'])
    prod_aux_data = prod_aux_data.drop_duplicates(subset = ['row_id'])
    prod_aux_data = prod_aux_data[[feat for feat in prod_aux_data.columns if '_y' not in feat]]
    prod_aux_data.columns = [feat.replace('_x','') for feat in prod_aux_data.columns]
    
    # removing already published records and selecting top 5 records
    prod_aux_data = prod_aux_data[prod_aux_data['posted']!=1].head(5)
    
    print('initiating request publish...')
    logger.info('initiating request publish...')
    counter = 0
    for index, row in prod_aux_data.iterrows():
        if row['posted'] != 1:
            twt_text = th.resource_generator(row)
            counter = counter + 1        
            print(counter)
            print(twt_text)
            if len(twt_text) <= 280:
                try:
                    # generating image
                    ic.create_img(row
                                  ,offset=700
                                  ,width=36
                                  ,image_path=image_path
                                  ,output_path=output_path
                                  ,font_path=font_path)
                    time.sleep(15)
                    # posting on TSI
                    print('publishing request on TSI...')
                    logger.info('publishing request on TSI...')
                    tsi_api.update_status(twt_text
                                          ,media_ids=th.attach_media_files(tsi_api
                                                                           ,output_path
                                                                           ,mode='single'))
                    # sending log to telegram
                    tp.send_message(tgram_token
                                        ,tgram_success_chatid
                                        ,'REQUEST POST - TeamSOSIndia - ' + twt_text)
                    # posting to CoPla
                    print('publishing request on CoPla...')
                    logger.info('publishing request on CoPla...')
                    #copla_api.update_status(twt_text)
                    copla_api.update_status(twt_text
                                            ,media_ids=th.attach_media_files(copla_api
                                                                             ,output_path
                                                                             ,mode='single'))
                    # sending log to telegram
                    tp.send_message(tgram_token
                                        ,tgram_success_chatid
                                        ,'REQUEST POST - CovidPlasamIn - ' + twt_text)
                except:
                    print('error encountered in posting...')
            
                time.sleep(random.randint(rand_sleep*60,(rand_sleep+sleep_lag)*60))

    print('finishing request publishing...')
    logger.info('finishing request publishing...')

    # setting all requests status to posted after posting each of them
    prod_aux_data['posted'] = 1
    
    # appending published records to aux_data
    # will be updated in google sheets
    aux_data = aux_data.append(prod_aux_data, ignore_index=True)

    # updating data in aux sheet
    try:
        print('starting data push to aux sheet...')
        logger.info('starting data push to aux sheet...')
        sheet = client.open(sheet_name)        

        # get the instance of the second sheet (aux)
        aux_sheet = sheet.get_worksheet(1)

        # refreshing aux sheet data
        set_with_dataframe(aux_sheet, aux_data)

        print('finishing data push to aux sheet...')
        logger.info('finishing data push to aux sheet...')
    except:
        print('error encountered with gsheet...')
        logger.info('error encountered...')