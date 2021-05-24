# -*- coding: utf-8 -*-
"""
Created on Fri May  7 19:18:02 2021

@author: rajat
"""

import pandas as pd
import numpy as np
from pygooglenews import GoogleNews
from newspaper import Article
from newspaper import Config
import joblib
from sklearn.feature_extraction.text import CountVectorizer
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe,get_as_dataframe
from covidplasma_bot.input import paths

# calling paths of vocab and model files
news_vocab_file = paths.news_vocab_file
news_model_file = paths.news_model_file
gsheet_json_file = paths.gsheet_json_file

def get_google_news():
    topic_search = ['COVID india','vaccine india', 'plasma india', 'COVID-19 india', 'hospital beds india', 'oxygen shortage india', 'remdesivir india']

    topic_set = []
    for topic in topic_search:
        googlenews=GoogleNews(lang='en', country = 'IN')
        result = googlenews.search(topic, when = '2h')
        #result = pd.DataFrame.from_dict(result, orient="index")
        cols = ['title', 'link', 'published']
        i =0 
        lst = []
        while i < len(result['entries']):
            title = result['entries'][i]['title']
            link = result['entries'][i]['link']
            published = result['entries'][i]['published']
            lst.append([title,link,published])
            i = i+1
    
        df1 = pd.DataFrame(lst, columns=cols)
        topic_set.append(df1)
        
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    config = Config()
    config.browser_user_agent = user_agent
    
    list=[]
    for df in topic_set: 
        for ind in df.index:
            try:
                dict={}
                article = Article(df['link'][ind],config=config)
                article.download()
                article.parse()
                article.nlp()
                dict['Date']=df['published'][ind]
                dict['Link']=df['link'][ind]
                dict['Title']=article.title
                dict['Article']=article.text
                dict['Summary']=article.summary
                list.append(dict)
            except:
                continue
    news_df=pd.DataFrame(list)
    return news_df

def get_df_with_processed_article(news_df):
    news_df['Article_Original'] = news_df['Article']

    ##Lower Case
    news_df['Article'] = news_df['Article'].str.lower()
    ##replace non-alphabetical characters with whitespaces
    news_df['Article'] = news_df['Article'].str.replace('[^a-zA-Z]', ' ')
    #corona_nlp_tweets
    ##ensure that the words of a message are separated by a single whitespace.
    news_df['Article'] = news_df['Article'].str.split()
    
    import requests
    stopwords = requests.get("https://raw.githubusercontent.com/fozziethebeat/S-Space/master/data/english-stop-words-large.txt").content.decode('utf-8').split('\n')
    from nltk.stem import PorterStemmer
    ps = PorterStemmer()
    
    articles = []
    
    for article in news_df['Article']:
        filtered_article = []
        for w in article: 
            if w not in stopwords: 
                filtered_article.append(ps.stem(w))
        articles.append(filtered_article)
        
    news_df['Article'] = articles
    
    news_df['Article'] = news_df['Article'].str.join(" ")
    return news_df

def lda_model(news_df):
    
    tf_features = pd.read_csv(news_vocab_file,header = None,names = ['vocab'])
    tf_vectorizer = CountVectorizer(max_df=0.95, min_df= 0.1, stop_words='english',ngram_range = (1, 3), vocabulary =  tf_features['vocab'])

    lda = joblib.load(news_model_file)

    tf = tf_vectorizer.fit_transform(news_df['Article'])
    doc_topic = lda.transform(tf)
    topic_most_pr = {}
    for n in range(doc_topic.shape[0]):
        topic_most_pr[n] = doc_topic[n].argmax(), doc_topic[n][doc_topic[n].argmax()]
    
    topic_doc = pd.DataFrame.from_dict(topic_most_pr, orient='index', columns = ['topic','topic_score'])
    news_df['Topic'] = topic_doc['topic']
    news_df['Topic_score'] = topic_doc['topic_score']
    
    # selecting 80th percentile as the cutoff score for Topic=3
    score_cutoff = news_df['Topic_score'][news_df['Topic']==3].quantile(0.8)
    
    # cut-off score for selecting topic 3 articles
    news_df['Label'] = np.where((news_df['Topic']==3) & (news_df['Topic_score']>=score_cutoff), 1, 0)
    #news_df['Label'] = np.where((news_df['Topic']==3) & (news_df['Topic_score']<score_cutoff), -1, 0)
    
    del news_df['Topic_score']
    
    return news_df

def write_gsheets(news_df):
    # define the scope
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    
    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name(gsheet_json_file, scope)
    
    # authorize the clientsheet 
    client = gspread.authorize(creds)
    
    # get the instance of the Spreadsheet
    sheet = client.open('COVIDNews')
    
    # get the first sheet of the Spreadsheet
    sheet_instance = sheet.get_worksheet(0)
    
    existing = get_as_dataframe(sheet_instance)
    news = news_df[['Link', 'Title', 'Date','Topic', 'Label']]
    updated = news.append(existing)
    
    set_with_dataframe(sheet_instance, updated)
    return 1