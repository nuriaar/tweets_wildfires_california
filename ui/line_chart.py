'''
Module creating the line chart visualization that display the number of
acres burned and number of tweets for the weeks of a given year.
'''

import sys
sys.path.append('../')

from resources.line_chart_preprocessing import get_plot_data, filter_plot_data
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def line_chart(year, fire_season = True):
    '''
    Creates a line chart of the tweet and wildfire intensity.

    Input:
        year (int): the year
        fire_season (bool): indicating whether only the fire season
            is relevant

    Output:
        line chart (fig): the plot
    '''
    plot_data = filter_plot_data(year, fire_season, get_plot_data())
    figure = make_subplots(specs = [[{'secondary_y': True}]])

    figure.add_trace(go.Scatter(\
        x = plot_data['week'], y = plot_data['nb_tweets'], \
            name = 'no. of tweets', line_color = '#1DA1F2'),\
            secondary_y = True,)
    figure.add_trace(go.Scatter(\
        x = plot_data['week'], y = plot_data['burned_acres'], \
            name = 'acres burned', line_color = '#ff2a04'),\
             secondary_y = False,)

    figure.update_layout(\
        title_text = f'Acres burned and tweet intensity in {year}', \
        title_font = dict(color = '#212121', size = 20))
    figure.update_xaxes(title_text = 'Week', showgrid = False, \
        color = '#212121', title_font_size = 18, fixedrange = True)
    figure.update_yaxes(title_text = 'Acres burned', secondary_y = False, \
        showgrid = False, color = '#ff2a04', title_font_size = 15, \
        fixedrange = True)
    figure.update_yaxes(title_text = 'No. of tweets', secondary_y = True, \
        showgrid = False, color = '#1DA1F2', title_font_size = 15, \
        fixedrange = True)
    figure.update_layout(paper_bgcolor = '#fff', plot_bgcolor = '#f5f7ff', \
        showlegend = False)

    return figure
