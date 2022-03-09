'''
Map Visualization of Wildfires
'''

import pandas as pd
import plotly.graph_objects as go

data_path = "data/wildfire_coordinate_data/"
years = ["2015", "2016", "2017", "2018", "2019", "2020", "2021"]
cols = ["fire_name", "gis_acres", "year", "alarm_date", "cont_date", "lat", "lon"]
coord_data = pd.DataFrame(columns = cols)

for year in years:
    coord_data_year = pd.read_csv(data_path + "clean_wildfires_data_" + year + ".csv")
    coord_data = pd.concat([coord_data, coord_data_year])

# Map
def map_wildfires(coord_data, year, fire_season):

    fig = go.Figure(go.Scattermapbox(
        mode = "lines", fill = "toself", fillcolor = "orange",
        lon = coord_data["lon"],
        lat = coord_data["lat"],
        name = "Wildfire",
        marker=go.scattermapbox.Marker(
                color = "red", size = 10),
        text = "<b>" + coord_data["fire_name"] + "</b><br>" +
                "GIS Acres: " + coord_data["gis_acres"].astype(str) + "<br>" +
                "Alarm date: " + coord_data["alarm_date"] + "<br>" +
                "Contingency date: " + coord_data["cont_date"],
        hovertemplate = "%{text}"
        ))

    fig.update_layout(
        mapbox = {'style': "stamen-terrain", 'center': {'lon': -119.4179, 'lat': 36.7783}, 'zoom': 5},
        showlegend = False,
        margin = {'l':0, 'r':0, 'b':0, 't':0})

    return fig



# ------ DASH ------

import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure = fig)
])

app.run_server(debug=True, use_reloader=False)
