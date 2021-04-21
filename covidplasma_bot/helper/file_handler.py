# -*- coding: utf-8 -*-
"""
@author:
    Verma, Himanshu
"""

import os

#----------------------------------------#
#Deleting existing log file
def del_log(path):
    if os.path.exists(path):
        os.remove(path)
    else:
        print("The file does not exist")

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