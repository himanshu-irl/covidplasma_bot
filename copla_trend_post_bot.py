# -*- coding: utf-8 -*-
"""
Created on Mon May 24 13:23:20 2021

@author: hverm
"""

import tweepy
import logging

#ud-modules
from covidplasma_bot.input import keys, paths
from covidplasma_bot.helper import file_handler as fh, telegram_poster as tp, tweet_handler as th
from covidplasma_bot.poster import tweet_poster as tpost
from covidplasma_bot.trends import covid_trends as ct

#Twitter API keys
CONSUMER_KEY = keys.CONSUMER_KEY
CONSUMER_SECRET = keys.CONSUMER_SECRET
ACCESS_KEY = keys.ACCESS_KEY
ACCESS_SECRET = keys.ACCESS_SECRET

#Telegram: TwitterNotify bot API keys
tgram_token = keys.tgram_token
tgram_success_chatid = keys.success_chatid #TwitterNotify Bot chat
tgram_error_chatid = keys.error_chatid # Twitter Bot Notifications channel

#Setting up paths
LOG_FILE_NAME = paths.trend_post_log_file

#----------------------------------------#

if __name__ == '__main__':
    try:
        print('deleting log file...')
        fh.del_log(LOG_FILE_NAME)
        logging.basicConfig(handlers=[logging.FileHandler(filename=LOG_FILE_NAME
                                                        ,encoding='utf-8'
                                                        ,mode='a+')]
                            ,level=logging.DEBUG
                            ,format='%(asctime)s %(message)s')
        logger = logging.getLogger(name='copla-trend-post-bot')

        tpost.post_tweet(CONSUMER_KEY
                            ,CONSUMER_SECRET
                            ,ACCESS_KEY
                            ,ACCESS_SECRET
                            ,tgram_token
                            ,tgram_success_chatid
                            ,logger
                            ,th.trend_txt(trend_df=ct.get_covid_data(logger)))
    
    except tweepy.TweepError as e:
        print(e)
        tp.send_message(tgram_token,tgram_error_chatid,str('COPLA - TREND BOT - ERROR: ' + str(e.args[0][0]['code']) + ' - ' + str(e.args[0][0]['message'])))
        logger.info(e)