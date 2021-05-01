# -*- coding: utf-8 -*-
"""
@author:
    Verma, Himanshu
"""

import tweepy
import os 
import random
from covidplasma_bot.input import tweet_parameter as param
#----------------------------------------#
#Udf for selecting random item from a list
def rand_item(ls):
    pop = len(ls)
    item = ls[random.randint(0,pop-1)]
    return item

#----------------------------------------#
#Udf for idenitfying if keywords exists in a string
def keywords_exists(key_list, string):
    exists = 0
    string = str(string.lower())
    for k in key_list:
        if k in string:
            exists = exists + 1
    
    return exists

#----------------------------------------#
#Udf for creating tweet text template
def reply_back(greet_list
               ,twt_user_name
               ,tweet_list
               ,publish_dtm
               ,trend_df
               ,hash_list
               ,tsi_check_flag=0
               ,case_id=0):
    greet_txt = rand_item(greet_list)
    twt_text = rand_item(tweet_list)
    
    if tsi_check_flag==0:
        twt_template = param.tweet_template
    else:
        twt_template = param.mention_reply_template
        
    #Getting covid KPI values
    deltaconfirmed_value = trend_df[trend_df['metric'] == 'deltaconfirmed']['value'].values[0]
    deltaconfirmed_trend = trend_df[trend_df['metric'] == 'deltaconfirmed']['trend'].values[0]
    deltarecovered_value = trend_df[trend_df['metric'] == 'deltarecovered']['value'].values[0]
    deltarecovered_trend = trend_df[trend_df['metric'] == 'deltarecovered']['trend'].values[0]
    deltadeaths_value = trend_df[trend_df['metric'] == 'deltadeaths']['value'].values[0]
    deltadeaths_trend = trend_df[trend_df['metric'] == 'deltadeaths']['trend'].values[0]
    totalactive_value = trend_df[trend_df['metric'] == 'totalactive']['value'].values[0]
    totalactive_trend = trend_df[trend_df['metric'] == 'totalactive']['trend'].values[0]
    tpr_value = trend_df[trend_df['metric'] == 'tpr']['value'].values[0]
    tpr_trend = trend_df[trend_df['metric'] == 'tpr']['trend'].values[0]
    hashtag = rand_item(hash_list)
    
    tweet_back = twt_template.replace('::greet::', greet_txt)
    tweet_back = tweet_back.replace('::user_name::', twt_user_name)
    tweet_back = tweet_back.replace('::twt_text::', twt_text)
    tweet_back = tweet_back.replace('::publish_dtm::', publish_dtm)
    #Trend values
    tweet_back = tweet_back.replace('::deltaconfirmed_value::', str(int(deltaconfirmed_value)))
    tweet_back = tweet_back.replace('::deltaconfirmed_trend::', str(deltaconfirmed_trend))
    tweet_back = tweet_back.replace('::deltarecovered_value::', str(int(deltarecovered_value)))
    tweet_back = tweet_back.replace('::deltarecovered_trend::', str(deltarecovered_trend))
    tweet_back = tweet_back.replace('::deltadeaths_value::', str(int(deltadeaths_value)))
    tweet_back = tweet_back.replace('::deltadeaths_trend::', str(deltadeaths_trend))
    tweet_back = tweet_back.replace('::totalactive_value::', str(int(totalactive_value)))
    tweet_back = tweet_back.replace('::totalactive_trend::', str(totalactive_trend))
    tweet_back = tweet_back.replace('::tpr_value::', str('{0:.3g}'.format(tpr_value)))
    tweet_back = tweet_back.replace('::tpr_trend::', str(tpr_trend))
    
    tweet_back = tweet_back.replace('::hashtag::', hashtag)
    
    if case_id > 0:
        tweet_back = tweet_back.replace('::case_id::', str(case_id))

    return tweet_back

#----------------------------------------#
#Udf for extracting friends of a twitter user
def get_friends_list(api,user_screen_name='CovidPlasmaIn'):
    friends_ls = []
    for frnd in tweepy.Cursor(api.friends, screen_name=user_screen_name).items():
        friends_ls.append(frnd.id)
        
    return friends_ls

#----------------------------------------#
#Udf for attaching media in a tweet
def attach_media_files(api, media_ls): 
    media_path = os.path.join('media',rand_item(media_ls))    
    media_list = list()
    response = api.media_upload(media_path)
    media_list.append(response.media_id_string)
    return media_list

#----------------------------------------#