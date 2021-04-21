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

## Files
mentions_log_file = os.path.join(log_path,'copla_mention_reply_bot.log')
replier_log_file = os.path.join(log_path,'copla_search_reply_bot.log')
mentions_file = os.path.join(data_path,'mentions_last_seen_id.txt')
replier_file = os.path.join(data_path,'replier_last_seen_id.txt')
covid_trend_file = os.path.join(data_path,'covid_trends_data.csv')