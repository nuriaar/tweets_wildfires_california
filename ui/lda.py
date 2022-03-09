import pandas as pd
from datetime import datetime
import gensim.corpora as corpora
from pprint import pprint
from resources.utils import read_data
import gensim
import plotly.graph_objects as go

def retrieve_topics(year, end_year, state_info = False, fire_season = False):
    '''
    '''

    tweets = read_data(year, state_info = False, fire_season = False)

    tweets['Text'] = tweets['Text'].astype(str).apply(lambda x: x.split())

    dictionary = corpora.Dictionary(tweets['Text'])
    texts = tweets['Text']
    corpus = [dictionary.doc2bow(text) for text in texts]

    num_topics = 3
    lda_model = gensim.models.LdaMulticore(corpus=corpus,
                                            id2word=dictionary,
                                            num_topics=num_topics)
    

    topics = lda_model.show_topics(3, 10, formatted = False)
    topics_words = [([word[0] for word in topic[1]]) for topic in topics]

    fig = go.Figure(data=[go.Table(header=dict(values=['Topic 1', 'Topic 2', 'Topic 3']),
                 cells=dict(values= topics_words))
                     ])
    fig.show()





https://plotly.com/python/table/