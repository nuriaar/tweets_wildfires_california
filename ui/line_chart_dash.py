import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()
app.layout = html.Div([
    dcc.Dropdown(id = 'year', options = [{'label': x, 'value': x} for x in [2015, 2016, 2017, 2018, 2019, 2020, 2021]], value = 2021),
    dcc.RadioItems(id = 'fire_season', options = [{'label': 'Entire Year', 'value': False}, {'label': 'Fire Season Only', 'value': True}], value = False),
    dcc.Graph(id = 'line_chart')
])

@app.callback(
    dash.dependencies.Output('line_chart', 'figure'),
    [dash.dependencies.Input('year', 'value'),
    dash.dependencies.Input('fire_season', 'value')])

### Add line_chart function here...

app.run_server(debug=True, use_reloader=False)