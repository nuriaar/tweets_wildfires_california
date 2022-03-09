'''
Dash Test - Núria
'''

import dash
import dash_html_components as html
import base64

from resources.utils import read_tweets_data, filter_coord_data, read_coord_data
from ui.tweets_analysis_viz import create_wordcloud, create_lda_table
from ui.map_viz import map_wildfires

tweets_data_filepath = "data/twitter_data/"
tweets_state_filename = "tweets_state.csv"
tweets_sample_filename = "sample_clean_data.csv"

tweets_state_data = read_tweets_data(tweets_data_filepath + tweets_state_filename)
tweets_sample_data = read_tweets_data(tweets_data_filepath + tweets_sample_filename)

# !!! get inputs for year, fire_season, state_info
if state_info:
    tweets = filter_coord_data(tweets_state_data, year, state_info, fire_season)
else:
    tweets = filter_coord_data(tweets_sample_data, year, state_info, fire_season)

# create wordcloud and save it as .png
create_wordcloud(tweets)
# create figure of lda table
lda_table = create_lda_table(tweets)


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

coord_data = read_coord_data()

# get year and fire_season inputs
map = map_wildfires(coord_data, year, fire_season)

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure = map)
])

app.run_server(debug=True, use_reloader=False)
