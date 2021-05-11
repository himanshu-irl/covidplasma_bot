# -*- coding: utf-8 -*-
"""
@author:
    Verma, Himanshu
"""

import os

#Setting up paths
## Folders
data_path = 'data'
media_path = 'media'
log_path = 'log'

# logs
mentions_log_file = os.path.join(log_path,'copla_mention_reply_bot.log')
replier_log_file = os.path.join(log_path,'copla_search_reply_bot.log')
news_log_file = os.path.join(log_path,'copla_news_post_bot.log')
news_refresh_log_file = os.path.join(log_path,'copla_news_refresh.log')
resource_post_log_file = os.path.join(log_path,'resource_post.log')

# NLP model files
news_model_file = os.path.join(data_path,'covid_news_model.sav')
news_vocab_file = os.path.join(data_path,'ModelVocab.csv')

# gsheet files
gsheet_json_file = os.path.join(data_path,'copla_gsheet_token.json')

# twitter files
mentions_file = os.path.join(data_path,'mentions_last_seen_id.txt')
replier_file = os.path.join(data_path,'replier_last_seen_id.txt')

# trend files
covid_trend_file = os.path.join(data_path,'covid_trends_data.csv')