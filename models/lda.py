import pandas as pd
import gensim.corpora as corpora
import gensim

def retrieve_topics(tweets):
    '''
    Retrieve main 3 topics from tweets (7 words per topic) and visualize a table

    Inputs:
        tweets: list of tweets

    Outputs:
        list of lists, with list of 7 words per topic
    '''

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

    return topics_words