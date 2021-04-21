# -*- coding: utf-8 -*-
"""
@author:
    Verma, Himanshu
"""

import pandas as pd
import requests as re
import json
from datetime import datetime, timedelta, date
import matplotlib.dates as mdates
import numpy as np

#User-defined modules
from covidplasma_bot.input import paths

#User-defined functions

#----------------------------------#
##Function to identify direction of trend
def trend_udf(x, y, order=1):
    x = mdates.date2num(list(x))
    coeffs = np.polyfit(x, list(y), order)
    slope = coeffs[-2]
    return float(slope)

#----------------------------------#
##Function to assign emoji to the trend
def trend_emoji(inp):
  if inp > 0:
    emoji = '🔼'
  else:
    emoji = '🔽'
  
  return emoji
#----------------------------------#

def get_covid_data(logger):
    #API source
    logger.info('getting data from covid19india.org API...')
    json_op = json.loads(re.get('https://api.covid19india.org/data.json').text)
    
    logger.info('converting data from json into dataframe...')
    cases_df = pd.DataFrame(json_op['cases_time_series'])
    tested_df = pd.DataFrame(json_op['tested'])
    states_df = pd.DataFrame(json_op['statewise'])

    # removing date column
    cases_df = cases_df[['dailyconfirmed', 'dailydeceased', 'dailyrecovered', 'dateymd',
       'totalconfirmed', 'totaldeceased', 'totalrecovered']]
    # renaming dateymd to date
    cases_df.columns = ['dailyconfirmed', 'dailydeceased', 'dailyrecovered', 'date',
       'totalconfirmed', 'totaldeceased', 'totalrecovered']

    #converting to datetime type
    logger.info('converting date & datetime columns into datetime datatype...')
    cases_df['date'] = cases_df['date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))
    #tested_df['updatetimestamp'] = tested_df['updatetimestamp'].apply(lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S'))
    states_df['lastupdatedtime'] = states_df['lastupdatedtime'].apply(lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S'))
    
    #Cleaning data - test data
    ## Renaming column and changing dtype
    logger.info('renaming columns...')
    tested_df = tested_df[tested_df['testedasof'] != '']
    tested_df.rename(columns = {'testedasof':'date'}, inplace = True)
    tested_df['date'] = tested_df['date'].apply(lambda x: datetime.strptime(x, '%d/%m/%Y'))
    #Trend is built on top of historical data from cases df (date-1)
    trend_df = cases_df[cases_df['date'] > (max(cases_df['date']) - timedelta(days=35))].reset_index(drop=True)
    
    #Adjust today's date according to timezone
    ## Check EC2's default timezone - UTC or IST?
    
    cases_cutoff_dtm = datetime.strptime((date.today().strftime("%d/%m/%Y") + ' 06:00:00'),'%d/%m/%Y %H:%M:%S')
    #cases_cutoff_dt = (date.today().strftime("%d/%m/%Y"))
    #print(cases_cutoff_dtm)
    
    #Converting columns to numeric
    states_df_cols = ['active', 'confirmed', 'deaths', 'deltaconfirmed', 'deltadeaths', 'deltarecovered', 'migratedother', 'recovered']
    states_df[states_df_cols] = states_df[states_df_cols].apply(pd.to_numeric)
    
    #Total active cases - published
    total_active_cases = states_df[states_df['state'] != 'Total'].sum(axis = 0, skipna = True)['active']
    
    latest_states_df = states_df[states_df['lastupdatedtime'] > cases_cutoff_dtm]
    latest_states_df = latest_states_df[latest_states_df['state'] != 'Total']
    
    #Latest delta of confirmed, recovered, deaths - published
    latest_states_sum_df = latest_states_df.sum(axis = 0, skipna = True)
    latest_deltaconfirmed = latest_states_sum_df['deltaconfirmed']
    latest_deltarecovered = latest_states_sum_df['deltarecovered']
    latest_deltadeaths = latest_states_sum_df['deltadeaths']
    
    print(total_active_cases, latest_deltaconfirmed,latest_deltarecovered,latest_deltadeaths)
    
    #Trend indicator generation
    ##Joining test data (tested_df) with consolidated cases_df
    trend_df = pd.merge(trend_df, tested_df, how = 'left', on='date')[['date', 'dailyconfirmed', 'dailydeceased', 'dailyrecovered', 'totalconfirmed', 'totaldeceased', 'totalrecovered', 'samplereportedtoday']]
    ##Changing dtypes - converting to numeric
    trend_df_cols = ['dailyconfirmed', 'dailydeceased', 'dailyrecovered', 'totalconfirmed', 'totaldeceased', 'totalrecovered', 'samplereportedtoday']
    trend_df[trend_df_cols] = trend_df[trend_df_cols].apply(pd.to_numeric)
    ##Adjusting tests reporting day difference
    trend_df['samplereportedtoday_lag'] = trend_df['samplereportedtoday'].shift(1)
    trend_df['tpr'] = trend_df.apply(lambda row: (row.dailyconfirmed/row.samplereportedtoday_lag)*100, axis=1)
    ##Creating active cases column
    trend_df['totalactive'] = trend_df.apply(lambda row: (row.totalconfirmed-row.totaldeceased-row.totalrecovered), axis=1)
    ##Calculating moving 7-day averages for metrics
    trend_df['dailyconfirmed_ma'] = trend_df['dailyconfirmed'].rolling(window=7).mean()
    trend_df['dailydeceased_ma'] = trend_df['dailydeceased'].rolling(window=7).mean()
    trend_df['dailyrecovered_ma'] = trend_df['dailyrecovered'].rolling(window=7).mean()
    trend_df['totalactive_ma'] = trend_df['totalactive'].rolling(window=7).mean()
    trend_df['tpr_ma'] = (trend_df['dailyconfirmed'].rolling(window=7).sum()/trend_df['samplereportedtoday_lag'].rolling(window=7).sum()).apply(lambda x: x*100)
    ##Publish L7D MA of TPR - published
    tpr_ma_publish = float(trend_df[trend_df['date'] == max(trend_df['date'])]['tpr_ma'])
    print(tpr_ma_publish)
    ##Filtering data to last 21 days
    trend_df = trend_df[trend_df['date'] > (max(trend_df['date']) - timedelta(days=21))].reset_index(drop=True)
    
    ##Creating trend emojies for metrics - published
    dailyconfirmed_trend = trend_emoji(trend_udf(trend_df['date'], trend_df['dailyconfirmed_ma']))
    dailydeceased_trend = trend_emoji(trend_udf(trend_df['date'], trend_df['dailydeceased_ma']))
    dailyrecovered_trend = trend_emoji(trend_udf(trend_df['date'], trend_df['dailyrecovered_ma']))
    active_trend = trend_emoji(trend_udf(trend_df['date'], trend_df['totalactive_ma']))
    tpr_trend = trend_emoji(trend_udf(trend_df['date'], trend_df['tpr_ma']))
    
    print(dailyconfirmed_trend, dailydeceased_trend, dailyrecovered_trend, tpr_trend, active_trend)
    
    #Creating metrics dataframe
    metrics_df = pd.DataFrame(columns=['metric','value','trend'])
    metrics_df = metrics_df.append(pd.Series(['deltaconfirmed',latest_deltaconfirmed,dailyconfirmed_trend], index = metrics_df.columns), ignore_index = True)
    metrics_df = metrics_df.append(pd.Series(['deltarecovered',latest_deltarecovered,dailydeceased_trend], index = metrics_df.columns), ignore_index = True)
    metrics_df = metrics_df.append(pd.Series(['deltadeaths',latest_deltadeaths,dailyrecovered_trend], index = metrics_df.columns), ignore_index = True)
    metrics_df = metrics_df.append(pd.Series(['totalactive',total_active_cases,active_trend], index = metrics_df.columns), ignore_index = True)
    metrics_df = metrics_df.append(pd.Series(['tpr',tpr_ma_publish,tpr_trend], index = metrics_df.columns), ignore_index = True)
    metrics_df['update_dtmz'] = datetime.now()
    print(metrics_df)
    
    if int(datetime.now().hour) in [12,1,2,3]:
        metrics_df = pd.read_csv(paths.covid_trend_file)
    else:
        metrics_df.to_csv(paths.covid_trend_file, index=False)
    
    return metrics_df