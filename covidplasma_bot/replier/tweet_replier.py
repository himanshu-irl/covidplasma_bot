# -*- coding: utf-8 -*-
"""
@author:
    Verma, Himanshu
"""
import tweepy
import time
import random
import datetime as dtm
from covidplasma_bot.helper import file_handler as fh, tweet_handler as th, telegram_poster as tp
from covidplasma_bot.input import tweet_parameter as param
from covidplasma_bot.trends import covid_trends as ct

#replier inputs
acc_filter = param.mentions_acc_filter
greet_list = param.greet_list
tweet_list = param.tweet_list
tsi_reply_list = param.tsi_reply_list
#publish_dtm = (dtm.datetime.now()+dtm.timedelta(hours=5.5)).strftime('%d %b %I%p')
hash_list = param.hash_list
mention_acc_check = param.mention_acc_check

def publish_dtm():
    return (dtm.datetime.now()+dtm.timedelta(hours=5.5)).strftime('%d %b %I%p')

def reply_to_tweets(CONSUMER_KEY
                    ,CONSUMER_SECRET
                    ,ACCESS_KEY
                    ,ACCESS_SECRET
                    ,tgram_token
                    ,tgram_success_chatid
                    ,logger
                    ,REPLIER_FILE_NAME
                    ,MENTION_FILE_NAME
                    ,search_for
                    ,date_since
                    ,rand_sleep
                    ,sleep_lag):
    
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
    last_seen_id = max(fh.retrieve_last_seen_id(REPLIER_FILE_NAME))
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
        mentions_last_seen_id_ls = fh.retrieve_last_seen_id(MENTION_FILE_NAME)
        replier_last_seen_id_ls = fh.retrieve_last_seen_id(REPLIER_FILE_NAME)
        engaged_tweet_ids = list(set(mentions_last_seen_id_ls).union(set(replier_last_seen_id_ls)))
        
        if twt_id not in engaged_tweet_ids:            
            if th.keywords_exists(param.filter_keywords, twt_user_name) == 0:
                if 'india' in str(twt_user_location).lower() or len(twt_user_location)==0:
                    if th.keywords_exists(param.txt_filter_keywords, twt_txt) == 0:
                        print(str(twt_id) + ' | ' + str(twt_user_name) + ' - ' + twt_txt, flush=True)
                        print('responding back...', flush=True)
                        logger.info('responding back...')
                        api.update_status(th.reply_back(greet_list
                                                        ,twt_user_name
                                                        ,tweet_list
                                                        ,publish_dtm = publish_dtm()
                                                        ,trend_df = ct.get_covid_data(logger)
                                                        ,hash_list = hash_list)
                                          ,twt_id
                                          ,auto_populate_reply_metadata=True
                                          ,media_ids=th.attach_media_files(api,param.media_ls))
                        #attachment_url='https://twitter.com/CovidPlasmaIn/status/1280240709048524800?s=20'
                        fh.store_last_seen_id(twt_id, REPLIER_FILE_NAME)
                        logger.info(str(twt_id) + ' - ' + twt_user_name)
                        tp.send_message(tgram_token,tgram_success_chatid,'COPLA SEARCH REPLY BOT - ' + str(twt_id) + ' - ' + str(twt_user_name) + ' - ' + str(twt_txt))
                        
                        #print('favoriting tweet...', flush=True)
                        #logger.info('favoriting tweet...')
                        #api.create_favorite(twt.id)
                        
                        #print('retweeting...', flush=True)
                        #logger.info('retweeting...')
                        #api.retweet(twt.id)
                        
                        #if twt.user.id not in friend_list:
                        
                            #print('following...', flush=True)
                            #logger.info('following...')
                            #api.create_friendship(twt.user.screen_name)
                            
                            #print('sending direct message...', flush=True)
                            #logger.info('sending direct message...')
                            #api.send_direct_message(twt.user.id,reply_back(True))
                        print('sleeping...', flush=True)
                        time.sleep(random.randint(rand_sleep*60,(rand_sleep+sleep_lag)*60))
                        

#----------------------------------------#
#Defining reply back function to engage with mentions
def reply_to_mentions(CONSUMER_KEY
                    ,CONSUMER_SECRET
                    ,ACCESS_KEY
                    ,ACCESS_SECRET
                    ,tgram_token
                    ,tgram_success_chatid
                    ,logger
                    ,REPLIER_FILE_NAME
                    ,MENTION_FILE_NAME
                    ,rand_sleep
                    ,sleep_lag):
    
    print('authenticating connection...')
    logger.info('authenticating connection...')
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

    print('retrieving already engaged tweet IDs...', flush=True)
    logger.info('retrieving already engaged tweet IDs...')    
    #max last seen id here
    max_last_seen_id = max(fh.retrieve_last_seen_id(MENTION_FILE_NAME))

    # NOTE: We need to use tweet_mode='extended' below to show
    # all full tweets (with full_text). Without it, long tweets
    # would be cut off.
    mentions = api.mentions_timeline(since_id = max_last_seen_id, tweet_mode='extended', count=5000)
    #Logged in user_name
    user_me = api.me().screen_name
    
    for mention in reversed(mentions):
        
        #Creating tweet variables        
        twt_id = mention.id
        in_reply_to_status_id = mention.in_reply_to_status_id
        mention_user_name = mention.user.screen_name
        mention_twt_txt = mention.full_text
        
        #Refresh tweet ID list
        #Union of mention and search reply tweet IDs to identify engaged tweets
        mentions_last_seen_id_ls = fh.retrieve_last_seen_id(MENTION_FILE_NAME)
        replier_last_seen_id_ls = fh.retrieve_last_seen_id(REPLIER_FILE_NAME)
        engaged_tweet_ids = list(set(mentions_last_seen_id_ls).union(set(replier_last_seen_id_ls)))
        
        if twt_id not in engaged_tweet_ids and mention_user_name not in acc_filter:
            if th.keywords_exists(param.txt_filter_keywords, mention_twt_txt) == 0:       
                mention_user_engaged = [u['screen_name'] for u in mention.entities['user_mentions']]
                mention_user_engaged.append(mention_user_name)
                mention_usr_eng_set = set(mention_user_engaged)

                mention_acc_flag = list(mention_usr_eng_set.intersection(mention_acc_check))

                common_users = []
                mention_last_twt_check = []
                reply_flag = False
                
                try:
                    print(twt_id,' - ',in_reply_to_status_id,' - ',mention_user_name,' - ',mention_twt_txt)
                    #If tweet is a reply to an already existing tweet
                    if in_reply_to_status_id is not None:
                        #Getting previous tweets details
                        in_reply_to_orig_tweet = api.get_status(id=in_reply_to_status_id, tweet_mode='extended')
                        
                        #Creating previous tweet's engaged tweets
                        user_engaged = [u['screen_name'] for u in in_reply_to_orig_tweet.entities['user_mentions']]
                        user_engaged.append(in_reply_to_orig_tweet.user.screen_name)
                        common_users = list(set(mention_user_engaged).intersection(user_engaged))
                        mention_last_twt_check = list(set(user_engaged).intersection(mention_acc_check))
                    
                    if user_me in common_users and len(common_users) > 0:
                        print('Already engaged...')
                    
                    elif len(common_users) > 0 and user_me in mention_user_engaged and user_me not in common_users:
                        print('reply to this tweet...')
                        reply_flag = True
                    
                    #when all mentioned users are not pulled in via tweepy and no intersection b/w old and new tweet (new: reply to old tweet)
                    elif len(common_users) > 0 and user_me not in common_users:
                        print('Already engaged...')
                    
                    #when tweet is a fresh one
                    elif len(common_users) == 0:
                        print('reply to this tweet...')
                        reply_flag = True
                    
                    if reply_flag:
                        if len(mention_acc_flag) > 0 or len(mention_last_twt_check) > 0:
                            # when tsi mentioned or mentioned in reply to an existing tweet
                            # normal template is followed
                            twt_inp_ls = tweet_list
                            tsi_check_flag = 0
                        else:
                            # tsi call is sent
                            twt_inp_ls = tsi_reply_list
                            tsi_check_flag = 1
                        
                        if tsi_check_flag == 1:
                            print('responding back...', flush=True)
                            logger.info('responding back...')
                            api.update_status(th.reply_back(greet_list
                                                            ,mention_user_name
                                                            ,twt_inp_ls
                                                            ,publish_dtm = publish_dtm()
                                                            ,trend_df = ct.get_covid_data(logger)
                                                            ,hash_list = hash_list
                                                            ,tsi_check_flag=tsi_check_flag
                                                            ,case_id=twt_id)
                                            ,twt_id
                                            ,auto_populate_reply_metadata=True
                                            ,media_ids=th.attach_media_files(api,param.media_ls))
                            logger.info(str(twt_id) + ' - ' + str(mention_user_name) + ' - ' + str(mention_twt_txt))
                            
                            tp.send_message(tgram_token,tgram_success_chatid,'COPLA MENTION REPLY BOT - ' + str(twt_id) + ' - ' + str(mention_user_name) + ' - ' + str(mention_twt_txt))
                                                
                            #Updating mentions tweet ID list
                            logger.info('storing tweet ID...')
                            fh.store_last_seen_id(twt_id, MENTION_FILE_NAME)
                            
                            time.sleep(random.randint(rand_sleep*60,(rand_sleep+sleep_lag)*60))
                except:
                    print('error encountered...')