import pandas as pd
from datetime import datetime
import gensim.corpora as corpora
from pprint import pprint
from resources.utils import read_data
import gensim
import plotly.graph_objects as go

def retrieve_topics(year, state_info = False, fire_season = False):
    '''
    Retrieve main 3 topics from tweets (7 words per topic) and visualize a table

    Inputs:
        year: (int) year to filter
        state_info: (str) "in" for California tweets, "out" for out of state tweets.
            If it's false, it retrieves all tweets (including those without location info)
        fire_season: (boolean) Include tweets only from Fire Season if true. Fire season goes
            from May to October included.
    
    Outputs:
        Plotly visualization (table)
    '''

    #read and filter data
    tweets = read_data(year, state_info = False, fire_season = False)
    tweets['Text'] = tweets['Text'].astype(str).apply(lambda x: x.split())

    #build corpus
    dictionary = corpora.Dictionary(tweets['Text'])
    texts = tweets['Text']
    corpus = [dictionary.doc2bow(text) for text in texts]

    #run LDA model
    num_topics = 3
    lda_model = gensim.models.LdaMulticore(corpus=corpus,
                                            id2word=dictionary,
                                            num_topics=num_topics)
    

    #extract topics
    topics = lda_model.show_topics(3, 7, formatted = False)
    topics_words = [([word[0] for word in topic[1]]) for topic in topics]

    #visualize topics
    fig = go.Figure(data=[go.Table(header=dict(values=['Topic 1', 'Topic 2', 'Topic 3']),
                 cells=dict(values= topics_words))
                     ])
    fig.show()

#read https://plotly.com/python/table/ at the bottom for Dash implementation