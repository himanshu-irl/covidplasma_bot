# -*- coding: utf-8 -*-
"""
@author:
    Verma, Himanshu
"""
import requests

#----------------------------------------#
#Udf for sending messages on telegram
def send_message(bot_token, bot_chatID, bot_message):
    
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + str(bot_message)
    response = requests.get(send_text)

    return response.json()