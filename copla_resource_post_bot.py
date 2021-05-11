# -*- coding: utf-8 -*-
"""
Created on Tue May 11 03:04:15 2021

@author: hverm
"""

import logging
import tweepy
import time
import random

#user-defined modules
from covidplasma_bot.input import keys, paths
from covidplasma_bot.helper import tweet_handler as th
from covidplasma_bot.helper import gsheet_handler as gh
from covidplasma_bot.helper import file_handler as fh
from covidplasma_bot.poster import tweet_poster as tp

# Twitter API Token
# TSI
CONSUMER_KEY = keys.CONSUMER_KEY
CONSUMER_SECRET = keys.CONSUMER_SECRET
ACCESS_KEY = keys.ACCESS_KEY
ACCESS_SECRET = keys.ACCESS_SECRET

# COPLA
CONSUMER_KEY_TSI = keys.CONSUMER_KEY_TSI
CONSUMER_SECRET_TSI = keys.CONSUMER_SECRET_TSI
ACCESS_KEY_TSI = keys.ACCESS_KEY_TSI
ACCESS_SECRET_TSI = keys.ACCESS_SECRET_TSI

copla_api = th.twt_conx_api(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)
tsi_api = th.twt_conx_api(CONSUMER_KEY_TSI, CONSUMER_SECRET_TSI, ACCESS_KEY_TSI, ACCESS_SECRET_TSI)

# Telegram: TwitterNotify bot API keys
tgram_token = keys.tgram_token
tgram_success_chatid = keys.success_chatid #TwitterNotify Bot chat
tgram_error_chatid = keys.error_chatid # Twitter Bot Notifications channel

#Setting up paths
LOG_FILE_NAME = paths.resource_post_log_file

# poster parameters
sheet_name = 'covid_resources'
cred = gh.ghsheet_cred()

while True:
    #deleting log file
    print('deleting log file...')
    fh.del_log(LOG_FILE_NAME)
    logging.basicConfig(handlers=[logging.FileHandler(filename=LOG_FILE_NAME
                                                      ,encoding='utf-8'
                                                      ,mode='a+')]
                        ,level=logging.DEBUG
                        ,format='%(asctime)s %(message)s')
    logger = logging.getLogger(name='resources-poster-bot')
    try:
        tp.resource_poster(sheet_name
                           ,cred
                           ,tsi_api
                           ,copla_api
                           ,tgram_token
                           ,tgram_success_chatid
                           ,logger
                           ,rand_sleep=1
                           ,sleep_lag=1)
        
    except tweepy.TweepError as e:
        print(e)
        tp.send_message(tgram_token,tgram_error_chatid,str('REQUEST POST - ERROR: ' + str(e.args[0][0]['code']) + ' - ' + str(e.args[0][0]['message'])))
        logger.info(e)
    time.sleep(random.randint(300,600))