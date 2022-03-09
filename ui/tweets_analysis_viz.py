'''
Tweets Text Analytics Visualizations
'''

from wordcloud import WordCloud
import plotly.graph_objects as go

from resources import retrieve_topics


def create_wordcloud(tweets):
    '''
    Create tweets word cloud visualization and save it in .png file.

    Inputs: 
        tweets (Pandas Dataframe): tweet data
    '''

    words = ' '.join(tweets['Text'].astype(str))

    wordcloud = WordCloud(
        background_color = 'white',
        max_words = 100,
        max_font_size = 30,
        scale = 3,
        random_state = 1)
   
    wordcloud = wordcloud.generate(str(words))

    create_wordcloud(tweets["Text"].tolist()).to_file('tweets_wordcloud.png')


def create_lda_table(tweets):
    
    topics_words = retrieve_topics(tweets)

    fig = go.Figure(
        data = [go.Table(
            header = {"values": ['Topic 1', 'Topic 2', 'Topic 3']},
            cells =  {"values": topics_words})
                     ])

    return fig

