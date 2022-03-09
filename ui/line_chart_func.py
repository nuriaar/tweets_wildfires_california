'''
TO DO:
    Get rid of warnings
    Assert fire_season
    Make graph pretty
    Filter on in- or out-of-state
'''
import sys
sys.path.append('../')

import pandas as pd
import matplotlib.pyplot as plt
from resources.line_chart_preprocessing import get_plot_data  ##Path: ../resources/line_chart_preprocessing.py
#import proj-larry_on_fire.resources.line_chart_preprocessing
import glob
#import plotly.graph_objects as go
#from plotly.subplots import make_subplots


def line_chart(year, fire_season = True):
    '''
    Creates a line chart of the tweet and wildfire intensity.

    Input:
        year (int): the year
        fire_season (bool): indicating whether only the fire season is relevant
    
    Ouptput:
        line chart (plt): the plot
    '''
    assert 2015 <= year <= 2021, 'Enter a year between 2015 and 2021'                                 #### DOUBLE CHECK WITH SERGIO
    assert type(fire_season) is bool, 'fire_season must be a boolean'

    plot_data = get_plot_data(year)

    if fire_season:
        plot_data = plot_data[18:45]
    
    fig, ax1 = plt.subplots()
    ax1.plot('week', 'acres', data = plot_data, color = 'red')
    ax2 = ax1.twinx()
    ax2.plot('week', 'nb_tweets', data = plot_data, color = 'blue')
    plt.title(f'Acres Burned and Tweet Intensity in {year}')
    ax1.set_xlabel('Week')
    ax1.set_ylabel('Burned Acres')
    ax2.set_ylabel('Number of Tweets')
    ax1.yaxis.label.set_color('red')
    ax2.yaxis.label.set_color('blue')
    plt.subplots_adjust(left = 0.15, right = 0.85, bottom = 0.15, top = 0.85)
    plt.savefig('test.png')
    return fig


#### Dash

# import dash
# import dash_core_components as dcc
# import dash_html_components as html

# app = dash.Dash()
# app.layout = html.Div([
#     dcc.Graph(figure=fig)
# ])

# app.run_server(debug=True, use_reloader=False)