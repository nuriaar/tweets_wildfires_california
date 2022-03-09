'''
Dash Test - Núria
'''

import dash
import dash_html_components as html
import base64

from resources.utils import read_tweets_data, filter_coord_data, read_coord_data
from ui.tweets_analysis_viz import create_wordcloud, create_lda_table
from ui.map_viz import map_wildfires

# LOAD DATA WHEN LOADING DASH - NO NEED TO REDO WITH CHANGING INPUTS

tweets_data_filepath = "data/twitter_data/"
tweets_state_filename = "tweets_state.csv"
tweets_sample_filename = "sample_clean_data.csv"

tweets_state_data = read_tweets_data(tweets_data_filepath + tweets_state_filename)
tweets_sample_data = read_tweets_data(tweets_data_filepath + tweets_sample_filename)
coord_data = read_coord_data()


# FILTER DATA ACCORDING TO USER INPUTS 
# !!! get inputs for year, fire_season, state_info

if state_info:
    tweets = filter_coord_data(tweets_state_data, year, state_info, fire_season)
else:
    tweets = filter_coord_data(tweets_sample_data, year, state_info, fire_season)

filtered_coord_data = filter_coord_data(coord_data, year, fire_season)

# CREATE DATA VISUALIZATIONS
create_wordcloud(tweets)
lda_table = create_lda_table(tweets)
map = map_wildfires(filtered_coord_data, year, fire_season)


# DASH 

# To show wordcloud –––––––––––––––––

app = dash.Dash()

# !!! if it's not showing, the path might be wrong
image_filepath = "ui/"
image_filename = 'tweets_wordcloud.png'
encoded_image = base64.b64encode(open(image_filepath + image_filename, 'rb').read())

app.layout = html.Div([
    html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))
])

if __name__ == '__main__':
    app.run_server()


# To show table see end of https://plotly.com/python/table/ –––––––––––––––––


# To show map –––––––––––––––––

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure = map)
])

app.run_server(debug=True, use_reloader=False)
