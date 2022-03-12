import dash
from dash import html
from dash import dcc
from dash import Input, Output
import plotly.express as px
import base64

from resources.utils import read_tweets_data, filter_coord_data,\
     read_coord_data, filter_tweets_data
from ui.tweets_analysis_viz import create_wordcloud, create_lda_table
from ui.map_viz import map_wildfires
from ui.line_chart import line_chart

# Loading preprocessed data
tweets_data_filepath = "data/twitter_data/"
tweets_state_filename = "tweets_state.csv"
tweets_sample_filename = "sample_clean_data.csv"

tweets_state_data = read_tweets_data(tweets_data_filepath + \
    tweets_state_filename)
tweets_sample_data = read_tweets_data(tweets_data_filepath + \
    tweets_sample_filename)
coord_data = read_coord_data()


### CREATING INITIAL DATA VISUALIZATIONS

## Geo map
filtered_coord_data = filter_coord_data(coord_data, year = 2020, \
    fire_season = True)
geo_map = map_wildfires(filtered_coord_data, year = 2020, \
    fire_season = True)

## Tweet line chart
tweet_plot = line_chart(year=2020, fire_season = True)


## Word cloud and LDA
filtered_tweets = filter_tweets_data(tweets_sample_data, state_info = False, \
    year = 2020, fire_season = True)

# Word cloud
create_wordcloud(filtered_tweets) # Word Cloud
image_filepath = "ui/"
image_filename = 'tweets_wordcloud.png'
encoded_image = base64.b64encode(open(image_filepath + image_filename,\
     'rb').read())

# LDA
lda_table = create_lda_table(filtered_tweets)


# Initialising the app
app = dash.Dash(__name__)

# Defining the app layout
app.layout = html.Div(
    children=[
        html.H2('Project Larry on Fire - Analyzing social media data \
            for wildfires in California, USA'),
        html.Div(className='Larry_Page',
            children=[
                html.Table(
                    [html.Tr(
                        [html.Td(
                            html.P('''Select a year:''')
                        ),
                        html.Td(
                            dcc.Dropdown(id = 'fire_year', options = \
                                [{'label': x, 'value': x} \
                                for x in [2015, 2016, 2017, 2018, 2019, 2020]], \
                                value = 2020)
                        )]
                    ),
                    html.Tr(
                            [html.Td(
                                html.P('''Select a season:''')
                            ),
                            html.Td(
                                dcc.RadioItems(id = 'fire_season', \
                                    options = [{'label': 'Entire Year', \
                                        'value': False}, {'label': 'Fire \
                                            Season Only', 'value': True}],\
                                                 value = True)
                            )]
                    ),
                    html.Tr(
                            [html.Td(
                                html.P('''Select a geography:''')
                            ),
                            html.Td(
                                dcc.RadioItems(id = 'state_info', \
                                    options = [{'label': 'Within state', \
                                        'value': "in"}, \
                                    {'label': 'Outside state', \
                                        'value': "out"},\
                                    {'label': 'All USA', 'value': False}], \
                                        value = False, inline=True)
                            )]
                    )]
            ),
            html.H3('Location and Twitter data analysis'),
            html.Table(
                    [html.Tr(
                            [html.Td(
                                dcc.Graph(id='geo_map', figure=geo_map
                                )
                            )]
                    ),
                    html.Tr(
                            [html.Td(
                                dcc.Graph(id='tweet_plot', figure=tweet_plot
                                )
                            )]
                    )]
            ),
            html.H3('Word cloud and LDA analysis'),
            html.Table(
                    [html.Tr(
                            [html.Td(
                                html.Div([html.Img(id="word_cloud", \
                                    src='data:image/png;base64,{}'.format(\
                                        encoded_image.decode()))
                                ])
                            )]
                    ),
                    html.Tr(
                            [html.Td(
                                dcc.Graph(id="lda_table", figure=lda_table
                                )
                            )]
                    )]

                )
            ]
        )
    ])

## Callbacks to update page dynamically

# Update Geo map
@app.callback(
    dash.dependencies.Output('geo_map', 'figure'),
    [dash.dependencies.Input('fire_year', 'value'),
    dash.dependencies.Input('fire_season', 'value')])
def update_geo_map(year, fire_season):
    filtered_coord_data = filter_coord_data(coord_data, year, fire_season)
    return map_wildfires(filtered_coord_data, year, fire_season)

# Update Tweet line chart
@app.callback(
    dash.dependencies.Output('tweet_plot', 'figure'),
    [dash.dependencies.Input('fire_year', 'value'),
    dash.dependencies.Input('fire_season', 'value')])
def update_tweet_line_chart(year, fire_season):
    return line_chart(year, fire_season)

# Update Word cloud
@app.callback(
    dash.dependencies.Output('word_cloud', 'src'),
    [dash.dependencies.Input('fire_year', 'value'),
    dash.dependencies.Input('fire_season', 'value'),
    dash.dependencies.Input('state_info', 'value')])
def update_word_cloud(year, fire_season, state_info):
    filtered_tweets = filter_tweets_data(tweets_sample_data, \
        state_info = state_info, year = year, fire_season = fire_season)
    create_wordcloud(filtered_tweets)
    image_filepath = "ui/"
    image_filename = 'tweets_wordcloud.png'
    encoded_image = base64.b64encode(open(image_filepath + \
        image_filename, 'rb').read())
    return 'data:image/png;base64,{}'.format(encoded_image.decode())


# Update LDA
@app.callback(
    dash.dependencies.Output('lda_table', 'figure'),
    [dash.dependencies.Input('fire_year', 'value'),
    dash.dependencies.Input('fire_season', 'value'),
    dash.dependencies.Input('state_info', 'value')])
def update_lda_chart(year, fire_season, state_info):
    filtered_tweets = filter_tweets_data(tweets_sample_data, \
        state_info = state_info, \
        year = year , fire_season = fire_season)
    return create_lda_table(filtered_tweets)


# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)
