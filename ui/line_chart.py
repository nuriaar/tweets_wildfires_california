import sys
sys.path.append('../')

import matplotlib.pyplot as plt
from resources.line_chart_preprocessing import get_plot_data, filter_plot_data
import plotly.graph_objects as go
from plotly.subplots import make_subplots


import dash
import dash_core_components as dcc
import dash_html_components as html


app = dash.Dash()
app.layout = html.Div([
    dcc.Dropdown(id = 'year', options = [{'label': x, 'value': x} for x in [2015, 2016, 2017, 2018, 2019, 2020, 2021]], value = 2021),
    dcc.RadioItems(id = 'fire_season', options = [{'label': 'Entire Year', 'value': False}, {'label': 'Fire Season Only', 'value': True}], value = False, labelStyle={'display': 'block'}),
    dcc.Graph(id = 'line_chart')
])

@app.callback(
    dash.dependencies.Output('line_chart', 'figure'),
    [dash.dependencies.Input('year', 'value'),
    dash.dependencies.Input('fire_season', 'value')])


def line_chart_proxy(year, fire_season = True):
    assert 2015 <= year <= 2021, 'Enter a year between 2015 and 2021'
    assert type(fire_season) is bool, 'fire_season must be a boolean'
    plot_data = filter_plot_data(year, fire_season, get_plot_data())
    return line_chart(year, plot_data)


def line_chart(year, plot_data):
    '''
    Creates a line chart of the tweet and wildfire intensity.

    Input:
        year (int): the year
        plot_data (pd.DataFrame): relevant data for the line chart

    Ouptput:
        line chart (fig): the plot
    '''
    figure = make_subplots(specs = [[{'secondary_y': True}]])
    figure.add_trace(go.Scatter(\
        x = plot_data['week'], y = plot_data['nb_tweets'], name = 'nb_tweets', line_color = '#1DA1F2'),\
            secondary_y = True,)
    figure.add_trace(go.Scatter(\
        x = plot_data['week'], y = plot_data['burned_acres'], name = 'burned_acres', line_color = '#ff2a04'),\
             secondary_y = False,)
    figure.update_layout(title_text = f'Acres Burned and Tweet Intensity in {year}', title_font = dict(color = '#FF8300', size = 30))
    figure.update_xaxes(title_text = 'Week', showgrid = False, color = '#D8D8D8', title_font_size = 30, fixedrange = True)
    figure.update_yaxes(title_text = 'Burned Acres', secondary_y = False, showgrid = False, color = '#ff2a04', title_font_size = 30, fixedrange = True)
    figure.update_yaxes(title_text = 'Number of Tweets', secondary_y = True, showgrid = False, color = '#1DA1F2', title_font_size = 30, fixedrange = True)
    figure.update_layout(
        paper_bgcolor = '#787878',
        plot_bgcolor = '#9A9A9A',
        showlegend = False)
    # fig.show()
    return figure


app.run_server(debug = True, use_reloader = False)
