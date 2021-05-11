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
# twitter api connection authenticator
def twt_conx_api(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET):
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

    return api
    
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
# generating resource text from template
def resource_generator(row):
    inp_dict = {}
    for index in list(row.index):
        value = str(row[index])
        inp_dict[index] = value
    
    # configuring info text
    info_txt = [inp_dict['info_txt_1'],inp_dict['info_txt_2'],inp_dict['info_txt_3']]
    info_txt = [x for x in info_txt if len(x.replace(' ',''))>0]
    info_txt = '\n'.join(info_txt)

    # configuring contact text
    contact_txt = [inp_dict['contact_1'],inp_dict['contact_2'],inp_dict['contact_3']]
    contact_txt = [x for x in contact_txt if len(x.replace(' ',''))==10]
    contact_txt = [f'{x} (wa.me/91{x})' for x in contact_txt]
    contact_txt = ', '.join(contact_txt)

    # configuring twitter handle
    if len(inp_dict['twt_handle'].replace(' ',''))>0:
        twt_handle = inp_dict['twt_handle'].replace(' ','')
        twt_handle = twt_handle.replace('@','')
        twt_handle = f'\nvia @{twt_handle}\n'

    else:
        twt_handle = ''

    twt_text = param.resource_template
    twt_text = twt_text.replace('::city::',inp_dict['city'])
    twt_text = twt_text.replace('::resource_type::',inp_dict['resource_type'])
    twt_text = twt_text.replace('::dtmz::',inp_dict['Timestamp'])
    twt_text = twt_text.replace('::info_txt::',info_txt)
    twt_text = twt_text.replace('::contact_txt::',contact_txt)
    twt_text = twt_text.replace('::twt_handle::',twt_handle)

    return twt_text