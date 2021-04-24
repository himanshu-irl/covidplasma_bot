# -*- coding: utf-8 -*-
"""
@author:
    Verma, Himanshu
"""

import os
from covidplasma_bot.input import paths

search_for = '(((plasma) (@CovidPlasmaIn OR @DelhiVsCorona OR @BloodDonorsIn OR @TeamSOSIndia OR @HydBloodDonors OR @CasesGurgaon)) OR ((plasma require) OR (need plasma donor) OR (need plasma recovered) OR (need covid plasma) OR (urgent covid plasma))) -"bit.ly" -from:RedCrossBloodGA -from:BloodDonorsIn -from:KABWelfare -from:TeamSOSIndia -from:CovidPlasmaIn -from:Blood_Matter -from:BloodAid -RT -Atlanta -filter:replies'
#covid OR OR recovered

greet_list = ['Hi','Hello','Hey','Namaste']

hash_list = ['#DonatePlasmaSaveALife','#plasmadonor','#COVID19','#COVID19India','#IndiaFightsCorona','#DonatePlasma','#SaveALife','#plasmatherapy'
            ,'#coronavirus','#TogetherWeCan','#plasmasaveslives','#PlasmaDonorHeroes','#plasma','#donateplasmaforhumanity','#indiacares'
            ,'#TwitterForGood','#PlasmaForIndia','#LetsFightCoronaTogether','#plasmadonation','#PlasmaMatters','#IndiaVsCorona','#IndiaVsCovid'
            ,'#PlasmaForIndia','#SpreadTheWord','#StopTheSpread','#LetsFightCorona','#TeamIndiaVsCovid']

tweet_list = ['Compiled list of available resources for getting in touch with COVID-19 recovered plasma donors'
            ,'If you are looking to connect with a COVID-19 recovered plasma donor, then please refer to the site'
            ,'Please refer to the compiled list of resources to connect with a COVID-19 recovered plasma donor'
            ,'25+ sources listed for connecting with COVID-19 recovered plasma donors'
            ,'Connect with potential COVID-19 recovered plasma donors using 25+ sources listed on this page'
            ,'Reach out to potential COVID-19 recovered plasma donors through portals, apps & contact details'
            ,'All the resources listed on this page are helping bridge the gap b/w patients & donors'
            ,'A compiled list of resources to help you connect to the COVID recovered plasma donors'
            ,'Consolidated list of available resources to match COVID-19 plasma recipients and donors']

tsi_reply_list = ['@TeamSOSIndia Could you please look into this request?'
                ,'@TeamSOSIndia Could you please look into this case?'
                ,'@TeamSOSIndia Could you kindly look into this case?'
                ,'@TeamSOSIndia Could you kindly look into this request?'
                ,'@TeamSOSIndia Kindly look into this request.'
                ,'@TeamSOSIndia Kindly look into this case.'
                ,'@TeamSOSIndia Please look into this request.'
                ,'@TeamSOSIndia Please look into this case.'
                ,'@TeamSOSIndia Requesting you to kindly look into this case.'
                ,'@TeamSOSIndia Requesting you to kindly look into this request.'
                ,'@TeamSOSIndia Requesting you to please look into this request.'
                ,'@TeamSOSIndia Requesting you to please look into this case.'
                ,'@TeamSOSIndia Requesting you to please assist.'
                ,'@TeamSOSIndia Requesting you to kindly assist.'
                ,'Adding @TeamSOSIndia for further assistance.'
                ,'Adding @TeamSOSIndia for further support.'
                ,'Tagging @TeamSOSIndia for further support.'
                ,'Tagging @TeamSOSIndia for further assistance.']

media_ls = os.listdir(paths.media_path)

filter_keywords = ['covidplasmain','madihafatima27','blood4pune','abhilasha1508','hydblooddonors'
                   ,'blooddonorsin','teamsosindia','theniteshsingh','raktnssdtu','kabwelfare'
                   ,'blood_matter','bloodaid','icansavelife']

txt_filter_keywords = ['blood4pune','SOSSaviours','sandhyafernez','rohit_4464','boomzy1231','DarshanNPopat','kalpeshvporwal1','INCaniketMhatre'
                       ,'manishJain1234','dial4242','indiacares_2020']

mentions_acc_filter = ['i_lakshay99','CasesGurgaon','architgupta99','dramebaz_woman'
                        ,'TheNeatSoul','TheNiteshSingh','FeedPPL','Sharmavs199'
                        ,'OberoiUgo','damodarpulpet','TeamSOSIndia'
                        ,'RaktaSatyagrah','TSIArmy','yuvahallabol']

mention_acc_check = ['TeamSOSIndia']

tweet_template = '''::greet:: ::user_name:: - ::twt_text::

Daily COVID-19 trends as of ::publish_dtm:: 🇮🇳:
+ve: ::deltaconfirmed_value::::deltaconfirmed_trend::
Recovery: ::deltarecovered_value::::deltarecovered_trend::
Death: ::deltadeaths_value::::deltadeaths_trend::
Tot. Active: ::totalactive_value::::totalactive_trend::
TPR (L7D Avg): ::tpr_value::::tpr_trend::

::hashtag::'''

mention_reply_template = '''::greet:: ::user_name:: - ::twt_text::

Daily COVID-19 trends as of ::publish_dtm:: 🇮🇳:
+ve: ::deltaconfirmed_value::::deltaconfirmed_trend::
Recovery: ::deltarecovered_value::::deltarecovered_trend::
Death: ::deltadeaths_value::::deltadeaths_trend::
Tot. Active: ::totalactive_value::::totalactive_trend::
TPR (L7D Avg): ::tpr_value::::tpr_trend::

::hashtag::'''