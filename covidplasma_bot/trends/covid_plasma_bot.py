# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 03:12:43 2020

@author: dB
"""
#If account is locked
#https://twitter.com/account/access

import tweepy
import time
import os 
import random
import datetime as dtm
import logging
import requests

#os.chdir('TwitterBot')

CONSUMER_KEY = 'TAmR61LVTjIB0XIPIfqWX4HZN'
CONSUMER_SECRET = '0jh5b4sCxLMoI0iehJoT5MdQellBQz1M9xtCl4OiXwjIcmDlZ7'
ACCESS_KEY = '1279502964311261184-JBLH9sS5pSCo3JkeX6UzQSLJv7iZEi'
ACCESS_SECRET = 'bNRJUbqlUprSYyriHxhPCtr7wjpqLv3fr39tensoMAbXn'

#Telegram: TwitterNotify bot API keys
tgram_bot_token = '1139518588:AAHwNk4qBxWTx3V_MfT6274GmQrijw2nOII'
tgram_bot_chatID_success = '617800051' #TwitterNotify Bot chat
tgram_bot_chatID_error = '-1001360445265' # Twitter Bot Notifications channel

date_since = (dtm.datetime.now()-dtm.timedelta(days=1)).strftime('%Y-%m-%d')

LOG_FILE_NAME = 'covid_plasma_bot.log'

#FILE_NAME = 'last_seen_id.txt'
MENTION_FILE_NAME = 'mentions_last_seen_id.txt'
REPLIER_FILE_NAME = 'replier_last_seen_id.txt'

search_for = '(((plasma) (@CovidPlasmaIn OR @DelhiVsCorona OR @BloodDonorsIn OR @TeamSOSIndia OR @HydBloodDonors OR @CasesGurgaon)) OR ((plasma require) OR (need plasma donor) OR (need plasma recovered) OR (need covid plasma) OR (urgent covid plasma))) -"bit.ly" -from:RedCrossBloodGA -from:BloodDonorsIn -from:KABWelfare -from:TeamSOSIndia -from:CovidPlasmaIn -from:Blood_Matter -from:BloodAid -RT -Atlanta -filter:replies'
#covid OR OR recovered

hash_list = ['#DonatePlasmaSaveALife','#plasmadonor','#COVID19','#COVID19India','#IndiaFightsCorona','#DonatePlasma','#SaveALife','#plasmatherapy'
            ,'#coronavirus','#TogetherWeCan','#plasmasaveslives','#PlasmaDonorHeroes','#plasma','#donateplasmaforhumanity','#indiacares'
            ,'#TwitterForGood','#PlasmaForIndia','#LetsFightCoronaTogether','#plasmadonation','#PlasmaMatters','#IndiaVsCorona','#IndiaVsCovid'
            ,'#PlasmaForIndia','#SpreadTheWord','#StopTheSpread','#LetsFightCorona']

tweet_list = ['Compiled list of available resources for getting in touch with COVID-19 recovered plasma donors.'
            ,'If you are looking to connect with a COVID-19 recovered plasma donor, then please refer to the site.'          
            ,'Please refer to the compiled list of resources to connect with a COVID-19 recovered plasma donor.'
            ,'25+ sources listed for connecting with COVID-19 recovered plasma donors.'
            ,'Connect with potential COVID-19 recovered plasma donors using 25+ sources listed on this page.'
            ,'Reach out to potential COVID-19 recovered plasma donors through portals, apps & contact details.'
            ,'All the resources listed on this page are helping bridge the gap b/w patients & donors.'
            ,'A compiled list of resources to help you connect to the COVID recovered plasma donors.'
            ,'Consolidated list of available resources to match COVID-19 plasma recipients and donors.']


page_link = ['t.co/sypouKUXae?amp=1','t.co/e4kf7eftMT?amp=1','t.co/YlP4zxGMZm?amp=1','t.co/pnfnoH90li?amp=1'
            ,'t.co/T3Lwl3zT5t?amp=1','t.co/OGQGdeKyJp?amp=1','t.co/hOtdxsP7bd?amp=1','t.co/akdMa8ouOx?amp=1'
            ,'t.co/ALxbLOTlwk?amp=1','t.co/vQEmn3OC5c?amp=1','t.co/8Q4lpPvji6?amp=1','t.co/5VhtnNMthE?amp=1'
            ,'t.co/phULCAZnoD?amp=1','t.co/qq8AcKhg7z?amp=1','t.co/Bx8zZWPzd6?amp=1','t.co/huo4IlLpbP?amp=1'
            ,'t.co/b6SWE9EnNx?amp=1','t.co/WRPuDFJPpn?amp=1','t.co/fT8EQFrKTM?amp=1','t.co/FBjg1Yqc8g?amp=1'
            ,'covidplasmain.page.link/q9Ku','covidplasmain.page.link/iGuj','covidplasmain.page.link/eNh4'
            ,'covidplasmain.page.link/Kz3a','covidplasmain.page.link/wv7o','covidplasmain.page.link/1'
            ,'covidplasmain.page.link/2','covidplasmain.page.link/3','covidplasmain.page.link/4'
            ,'covidplasmain.page.link/5','covidplasmain.page.link/6','covidplasmain.page.link/7'
            ,'covidplasmain.page.link/8','covidplasmain.page.link/9','covidplasmain.page.link/10']

media_ls = ['1.png','2.png','3.png','4.png','5.png','6.png','7.png','8.png'
            ,'1.gif','2.gif','3.gif','4.gif','5.gif','6.gif','7.gif','8.gif']

filter_keywords = ['covidplasmain'
                   ,'madihafatima27'
                   ,'blood4pune'
                   ,'abhilasha1508'
                   ,'hydblooddonors'
                   ,'blooddonorsin'
                   ,'teamsosindia'
                   ,'theniteshsingh'
                   ,'raktnssdtu'
                   ,'kabwelfare'
                   ,'blood_matter'
                   ,'bloodaid'
                   ,'icansavelife']

txt_filter_keywords = ['blood4pune','SOSSaviours','sandhyafernez','rohit_4464','boomzy1231','DarshanNPopat','kalpeshvporwal1','INCaniketMhatre'
                       ,'manishJain1234','dial4242','indiacares_2020']
                   
#----------------------------------------#
def del_log():
    if os.path.exists('covid_plasma_bot.log'):
        os.remove('covid_plasma_bot.log')
    else:
        print("The file does not exist")

#----------------------------------------#
def rand_item(ls):
    pop = len(ls)
    item = ls[random.randint(0,pop-1)]
    return item

#----------------------------------------#
def reply_back(link=False):
    twt_text = rand_item(tweet_list)
    hastag = rand_item(hash_list)
    page_lnk = rand_item(page_link)
    
    if link:
        tweet_back = 'COVID-19 plasma therapy resources for India\n\n'+twt_text+ ' ' +page_lnk+'\n\n'+hastag
    else:
        tweet_back = 'COVID-19 plasma therapy resources for India\n\n'+twt_text +' Check bio for details. @TeamSOSIndia @TheNiteshSingh @himanshu_irl'+'\n\n'+hastag
    
    return tweet_back

#----------------------------------------#
#Retrieving last engaged tweet IDs
def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id_ls = f_read.read().split('\n')
    last_seen_id_ls = [int(x) for x in last_seen_id_ls if len(x) > 0]
    f_read.close()
    return last_seen_id_ls
    
#----------------------------------------#
#Storing engaged tweet's ID
def store_last_seen_id(last_seen_id, file_name):
    with open(file_name, 'a') as f:
        f.write('%d\n' % last_seen_id)
    
    print('Tweet ID: {} - appeneded...'.format(last_seen_id))

#----------------------------------------#
def telegram_bot_sendtext(bot_token, bot_chatID, bot_message):
    
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + str(bot_message)
    response = requests.get(send_text)

    return response.json()

#----------------------------------------#   
def get_friends_list(api,user_screen_name='CovidPlasmaIn'):
    friends_ls = []
    for frnd in tweepy.Cursor(api.friends, screen_name=user_screen_name).items():
        friends_ls.append(frnd.id)
        
    return friends_ls

#----------------------------------------#
def attach_media_files(api,ls_media): 
    media_path = os.path.join('media',rand_item(media_ls))    
    media_list = list()
    response = api.media_upload(media_path)
    media_list.append(response.media_id_string)
    return media_list

#----------------------------------------#
def keywords_exists(key_list, string):
    exists = 0
    string = str(string.lower())
    for k in key_list:
        if k in string:
            exists = exists + 1
    
    return exists

#----------------------------------------#
def reply_to_tweets():
    
    print('authenticating connection...')
    logger.info('authenticating connection...')
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
    
    #print('getting friends list...')
    #logger.info('getting friends list...')
    #friend_list = get_friends_list(api)
    
    print('retrieving and replying to tweets...', flush=True)
    logger.info('retrieving and replying to tweets...')
    # DEV NOTE: use 1060651988453654528 for testing.
    #last_seen_id = retrieve_last_seen_id(FILE_NAME)
    last_seen_id = max(retrieve_last_seen_id(REPLIER_FILE_NAME))
    # NOTE: We need to use tweet_mode='extended' below to show
    # all full tweets (with full_text). Without it, long tweets
    # would be cut off.
    twts = api.search(q=search_for,since=date_since,result_type='recent',since_id = last_seen_id,count=20000)
    
    #twts = tweepy.Cursor(api.search, q=(search_for),lang="en", since=date_since,since_id = last_seen_id).items(10000)
    
    for twt in reversed(twts):

        #Creating tweet variables        
        twt_id = twt.id
        twt_user_name = twt.user.screen_name
        twt_user_location = twt.user.location
        twt_txt = twt.text
        
        #Refresh tweet ID list
        #Union of mention and search reply tweet IDs to identify engaged tweets
        mentions_last_seen_id_ls = retrieve_last_seen_id(MENTION_FILE_NAME)
        replier_last_seen_id_ls = retrieve_last_seen_id(REPLIER_FILE_NAME)
        engaged_tweet_ids = list(set(mentions_last_seen_id_ls).union(set(replier_last_seen_id_ls)))
        
        if twt_id not in engaged_tweet_ids:
            store_last_seen_id(twt_id, REPLIER_FILE_NAME)
            
            if keywords_exists(filter_keywords, twt_user_name) == 0:
                if 'india' in str(twt_user_location).lower() or len(twt_user_location)==0:
                    if keywords_exists(txt_filter_keywords, twt_txt) == 0:
                        print(str(twt_id) + ' | ' + str(twt_user_name) + ' - ' + twt_txt, flush=True)
                        print('responding back...', flush=True)
                        logger.info('responding back...')
                        api.update_status('@' + twt_user_name + ' ' +reply_back(False), twt_id,auto_populate_reply_metadata=True,media_ids=attach_media_files(api,media_ls))
                        #attachment_url='https://twitter.com/CovidPlasmaIn/status/1280240709048524800?s=20'
                        
                        logger.info(str(twt_id) + ' - ' + twt_user_name)
                        telegram_bot_sendtext(tgram_bot_token,tgram_bot_chatID_success,str(twt_id) + ' - ' + twt_user_name + ' - ' + str(twt_txt))
                        
                        print('favoriting tweet...', flush=True)
                        logger.info('favoriting tweet...')
                        #api.create_favorite(twt.id)
                        
                        print('retweeting...', flush=True)
                        logger.info('retweeting...')
                        #api.retweet(twt.id)
                        
                        #if twt.user.id not in friend_list:
                        
                            #print('following...', flush=True)
                            #logger.info('following...')
                            #api.create_friendship(twt.user.screen_name)
                            
                            #print('sending direct message...', flush=True)
                            #logger.info('sending direct message...')
                            #api.send_direct_message(twt.user.id,reply_back(True))
                        
                        time.sleep(random.randint(480,720))

# while True:
#     reply_to_tweets()
#     print('Twitter error!')
#     time.sleep(random.randint(400,600))

while True:
    #deleting log file
    print('deleting log file...')
    del_log()
    logging.basicConfig(filename=LOG_FILE_NAME, level=logging.DEBUG,format='%(asctime)s %(message)s')
    logger = logging.getLogger(name='covid-plasma-bot')
    try:
        reply_to_tweets()
    except tweepy.TweepError as e:
        print(e)
        telegram_bot_sendtext(tgram_bot_token,tgram_bot_chatID_error,str('ERROR: ' + str(e.args[0][0]['code']) + ' - ' + str(e.args[0][0]['message'])))
        logger.info(e)
    time.sleep(random.randint(300,600)) #200,300