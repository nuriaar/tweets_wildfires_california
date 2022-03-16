'''
Tweets text analytics preprocessing.
'''

import pandas as pd
import nltk
import regex as re

from os import listdir
from datetime import datetime
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords


nltk.download('stopwords')
stopwords = stopwords.words('english')
stopwords.extend(["california", "wildfires", "wildfire", "californias", "via",
                    "amp", "fire", "fires"])

def transform_all_tweets(stopwords, stem = False):
    '''
    Read and combine all CSV files that start with a digit in twitter_data, 
    clean text data to extract relevant tokens for text analysis, and write 
    a CSV with a  random sample of 500,000 tweets, and a CSV with tweets that 
    contain State information.

    Inputs:
        stopwords (list): stop words to be removed
        stem (boolean): indicates if we want to apply stemming
    '''

    all_tweets = pd.DataFrame()
    path = "data/twitter_data/"
    filenames = listdir(path)

    dateparse = lambda x: datetime.strptime(x, '%Y-%m-%d')

    for name in filenames:
        print(name)
        if bool(re.match("\d.*.csv", name)):
            df = pd.read_csv(path + name, parse_dates = ['Date'], date_parser = dateparse)
            df['Text'] = clean_tweets(df['Text'], stopwords, stem)
            if all_tweets.empty:
                all_tweets = df
            else:
                all_tweets = pd.concat([all_tweets, df], ignore_index = True)

    sample = all_tweets.sample(n = 500000)
    sample.to_csv("data/twitter_data/sample_clean_data.csv")

    tweets_state = all_tweets.dropna()
    tweets_state.to_csv('data/twitter_data/tweets_state.csv')


def clean_tweets(col, stopwords, stem = False):
    '''
    For the the text column of a dataframe with twitter info, 
    clean text and return a list of cleaned tokens. 

    Inputs:
        col (Pandas Series): text column
        stem (boolean): if we want to reduce tokens to stems
        stopwords (list): stop words to remove
    
    Output:
        (Pandas Series) text column with clean data
    '''

    col = col.str.replace('RT', '')\
        .str.replace('@[\w]+','')\
        .str.replace('http\S+', '')\
        .str.replace('[^\w\s]', '')\
        .str.replace('\d+','')\
        .str.lower()\
        .str.split()

    if stem:
        st = PorterStemmer()
        col = col.apply(lambda x: " ".join([st.stem(word) for word in x if not word in stopwords]))
    else:
        col = col.apply(lambda x: " ".join([word for word in x if not word in stopwords]))

    return col
