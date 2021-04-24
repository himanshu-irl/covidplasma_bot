# -*- coding: utf-8 -*-
"""
@author:
    Verma, Himanshu
"""
#If account is locked
#https://twitter.com/account/access

import tweepy
import time
import random
import datetime as dtm
import logging

#ud-modules
from covidplasma_bot.input import keys, paths, tweet_parameter as param
from covidplasma_bot.replier import tweet_replier as tr
from covidplasma_bot.helper import file_handler as fh, telegram_poster as tp

#Twitter API keys
CONSUMER_KEY = keys.CONSUMER_KEY
CONSUMER_SECRET = keys.CONSUMER_SECRET
ACCESS_KEY = keys.ACCESS_KEY
ACCESS_SECRET = keys.ACCESS_SECRET

#Telegram: TwitterNotify bot API keys
tgram_token = keys.tgram_token
tgram_success_chatid = keys.success_chatid #TwitterNotify Bot chat
tgram_error_chatid = keys.error_chatid # Twitter Bot Notifications channel

date_since = (dtm.datetime.now()-dtm.timedelta(days=1)).strftime('%Y-%m-%d')

#Setting up paths
LOG_FILE_NAME = paths.replier_log_file
#FILE_NAME = 'last_seen_id.txt'
MENTION_FILE_NAME = paths.mentions_file
REPLIER_FILE_NAME = paths.replier_file

#----------------------------------------#

while True:
    #deleting log file
    print('deleting log file...')
    fh.del_log(LOG_FILE_NAME)
    logging.basicConfig(handlers=[logging.FileHandler(filename=LOG_FILE_NAME
                                                      ,encoding='utf-8'
                                                      ,mode='a+')]
                        ,level=logging.DEBUG
                        ,format='%(asctime)s %(message)s')
    logger = logging.getLogger(name='copla-search-reply-bot')
    try:
        tr.reply_to_tweets(CONSUMER_KEY
                           ,CONSUMER_SECRET
                           ,ACCESS_KEY
                           ,ACCESS_SECRET
                           ,tgram_token
                           ,tgram_success_chatid
                           ,logger
                           ,REPLIER_FILE_NAME
                           ,MENTION_FILE_NAME
                           ,search_for = param.search_for
                           ,date_since = date_since
                           ,rand_sleep=6)
    except tweepy.TweepError as e:
        print(e)
        tp.send_message(tgram_token,tgram_error_chatid,str('COVID PLASMA BOT REPLIER ERROR: ' + str(e.args[0][0]['code']) + ' - ' + str(e.args[0][0]['message'])))
        logger.info(e)
    time.sleep(random.randint(300,600))