#part of preprocessing data
import pandas as pd
import glob
from os import listdir
import regex as re
from datetime import datetime
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')

all_tweets = pd.DataFrame()
path = "data/"
filenames = listdir("data/")

dateparse = lambda x: datetime.strptime(x, '%Y-%m-%d')

stopwords = stopwords.words('english')
stopwords.extend(["california", "wildfires", "wildfire", "californias", "via",
                    "amp", "fire", "fires"])

for name in filenames:
    print(name)
    if bool(re.match("\d.*.csv", name)):
        df = pd.read_csv(path + name, parse_dates = ['Date'], date_parser = dateparse)
        df['Text'] = cleaning_data(df['Text'], stopwords)
        if all_tweets.empty:
            all_tweets = df
        else:
            all_tweets = pd.concat([all_tweets, df], ignore_index = True)

sample = all_tweets.sample(n=500000)
sample.to_csv("data/sample_clean_data.csv")

tweets_state = all_tweets.dropna()
tweets_state.to_csv('data/tweets_state.csv')

import gensim.corpora as corpora
dictionary = corpora.Dictionary(all_tweets['Text'])
texts = all_tweets['Text']

corpus = [dictionary.doc2bow(text) for text in texts]

from pprint import pprint
    # number of topics
    num_topics = 10
    # Build LDA model
    lda_model = gensim.models.LdaMulticore(corpus=corpus,
                                            id2word=dictionary,
                                            num_topics=num_topics)

 doc_lda = lda_model[corpus]    

 def cleaning_data(col, stopwords, stem = False):
    '''
     For the the text column of a dataframe with twitter info, 
     clean text and return a list of cleaned tokens. 

     Inputs:
        col: text column
        stem: boolean if we want to reduce tokens to stems
        stopwords: list of words to remove
    
    Output:
        text column with clean data
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
        col = col.apply(lambda x: [st.stem(word) for word in x if not word in stopwords])
    else:
        col = col.apply(lambda x: [word for word in x if not word in stopwords])
    
    return col