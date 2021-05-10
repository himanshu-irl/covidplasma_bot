# -*- coding: utf-8 -*-
"""
@author:
    Verma, Himanshu
"""
import tweepy
from covidplasma_bot.helper import telegram_poster as tp

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