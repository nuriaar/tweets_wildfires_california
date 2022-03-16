'''
Latent Dirichlet Allocation analysis of Twitter data.
'''

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation


def retrieve_topics(tweets):
    '''
    Retrieve main 3 topics from tweets (7 words per topic)

    Inputs:
        tweets (list of strings)

    Outputs:
        list of lists, with list of 7 words per topic
    '''

    vect = TfidfVectorizer(max_features = 1000)
    vect_text = vect.fit_transform(tweets['Text'].astype(str))
    idf = vect.idf_
    lda_model = LatentDirichletAllocation(n_components = 3, max_iter = 1)
    lda_top = lda_model.fit_transform(vect_text)
    features = vect.get_feature_names_out()

    words_topics = []
    for _, comp in enumerate(lda_model.components_):
        vocab_comp = zip(features, comp)
        sorted_words = sorted(vocab_comp, key = lambda x:x[1], reverse = True)[:7]
        tmp_ls = []
        for word, _ in sorted_words:
            tmp_ls.append(word)
        words_topics.append(tmp_ls)

    return words_topics
