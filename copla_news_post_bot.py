# -*- coding: utf-8 -*-
"""
Created on Sat May  8 18:54:12 2021

@author: hverm
"""

import tweepy
import logging

#ud-modules
from covidplasma_bot.input import keys, paths
from covidplasma_bot.helper import file_handler as fh, telegram_poster as tp
from covidplasma_bot.news import post_news

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
LOG_FILE_NAME = paths.news_log_file

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
        logger = logging.getLogger(name='copla-news-post-bot')
        post_news.news_post(CONSUMER_KEY
                            ,CONSUMER_SECRET
                            ,ACCESS_KEY
                            ,ACCESS_SECRET
                            ,tgram_token
                            ,tgram_success_chatid
                            ,logger
                            ,post_news.get_news_from_gsheets())

    except tweepy.TweepError as e:
        print(e)
        tp.send_message(tgram_token,tgram_error_chatid,str('COPLA - NEWS BOT - ERROR: ' + str(e.args[0][0]['code']) + ' - ' + str(e.args[0][0]['message'])))
        logger.info(e)