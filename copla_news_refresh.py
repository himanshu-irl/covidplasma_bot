# -*- coding: utf-8 -*-
"""
Created on Sat May  8 18:54:12 2021

@author: hverm
"""

import logging

#ud-modules
from covidplasma_bot.input import keys, paths
from covidplasma_bot.replier import tweet_replier as tr
from covidplasma_bot.helper import file_handler as fh, telegram_poster as tp
from covidplasma_bot.news import news_refresh as nr

#Telegram: TwitterNotify bot API keys
tgram_token = keys.tgram_token
tgram_success_chatid = keys.success_chatid #TwitterNotify Bot chat
tgram_error_chatid = keys.error_chatid # Twitter Bot Notifications channel

#Setting up paths
LOG_FILE_NAME = paths.news_refresh_log_file

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
        logger.info('getting latest news...')
        news_df = nr.get_google_news()
        logger.info('processing news to data...')
        news_df = nr.get_df_with_processed_article(news_df)
        logger.info('running model to categorize news...')
        news_df = nr.lda_model(news_df)
        logger.info('writing data to google sheet...')
        nr.write_gsheets(news_df)

    except:
        tp.send_message(tgram_token,tgram_error_chatid,str('COPLA - NEWS REFRESH - ERROR: News not updated!'))
        logger.info('ERROR: News not updated!')