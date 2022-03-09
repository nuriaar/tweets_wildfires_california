import pandas as pd
from datetime import datetime
import gensim.corpora as corpora
from pprint import pprint
from resources.utils import read_data

def retrieve_topics(start_year, end_year, state_info = False, fire_season = False):
    '''
    '''

    tweets = read_data(start_year, end_year, state_info = False, fire_season = False)

    dictionary = corpora.Dictionary(tweets['Text'])
    texts = tweets['Text']
    corpus = [dictionary.doc2bow(text) for text in texts]
    doc_lda = lda_model[corpus] 

    
    num_topics = 4
    lda_model = gensim.models.LdaMulticore(corpus=corpus,
                                            id2word=dictionary,
                                            num_topics=num_topics)

    doc_lda = lda_model[corpus]    