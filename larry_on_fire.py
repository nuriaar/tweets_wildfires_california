import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px

from resources.utils import read_tweets_data, filter_coord_data, read_coord_data, filter_tweets_data
from ui.tweets_analysis_viz import create_wordcloud, create_lda_table
from ui.map_viz import map_wildfires

# Loading preprocessed data
tweets_data_filepath = "data/twitter_data/"
tweets_state_filename = "tweets_state.csv"
tweets_sample_filename = "sample_clean_data.csv"

tweets_state_data = read_tweets_data(tweets_data_filepath + tweets_state_filename)
tweets_sample_data = read_tweets_data(tweets_data_filepath + tweets_sample_filename)
coord_data = read_coord_data()


# Creating initial data visualizations
filtered_tweets = filter_tweets_data(tweets_sample_data, state_info = False, year = 2021, fire_season = True)
filtered_coord_data = filter_coord_data(coord_data, year = 2021, fire_season = True)
create_wordcloud(filtered_tweets)
lda_table = create_lda_table(filtered_tweets)
map = map_wildfires(filtered_coord_data)

# Initialising the app
app = dash.Dash(__name__)

# Defining the app
app.layout = html.Div(
        children=[
                html.H2('Project Larry on Fire - Analyzing social media data for wildfires in California, USA'),
                html.Div(className='row-1',  # Define the first row element
                        children=[
                                html.Table(
                                        [html.Tr(
                                                [html.Td(
                                                        html.P('''Select a year:''')
                                                ),
                                                html.Td(
                                                        dcc.Dropdown(id = 'year', options = [{'label': x, 'value': x} \
                                                                for x in [2015, 2016, 2017, 2018, 2019, 2020, 2021]], \
                                                                value = 2021)
                                                )]
                                        ),
                                        html.Tr(
                                                [html.Td(
                                                        html.P('''Select a season:''')
                                                ),
                                                html.Td(
                                                        dcc.RadioItems(id = 'fire_season', \
                                                                options = [{'label': 'Entire Year', 'value': False}, \
                                                                {'label': 'Fire Season Only', 'value': True}], value = False)
                                                )]
                                        ),
                                        html.Tr(
                                                [html.Td(
                                                        html.P('''Select a geography:''')
                                                ),
                                                html.Td(
                                                        dcc.RadioItems(
                                                                ['In state', 'Outside state', 'All USA'],
                                                                'All USA', inline=True)
                                                )]
                                        )]

                                ),
                                html.H3('Location and Twitter data analysis'),
                                html.Table(
                                        [html.Tr(
                                                [html.Td(
                                                        html.Div(className='Maps')
                                                )]
                                        ),
                                        html.Tr(
                                                [html.Td(
                                                        html.Div(className='Plot')
                                                )]
                                        )]

                                )
                                ,  # Define the Maps element
                                  # Define the Plot element
                        ]
                ),
                html.Div(className='row-2',  # Define the second row element
                        children=[
                                html.H3('Word cloud and LDA analysis'),
                                html.Table(

                                ),
                                html.Div(className='Word Cloud'),  # Define the Maps element
                                html.Div(className='LDA')  # Define the Plot element
                        ]
                ),
        ])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
