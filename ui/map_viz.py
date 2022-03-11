'''
Map Visualization of Wildfires
'''

import plotly.express as px

from resources.utils import filter_coord_data

def map_wildfires(coord_data, year, fire_season):
    '''
    Create mapbox wildfire visualization. 

    Inputs:
        coord_data (GeoPandas Dataframe): wildfire data including polygon 
            coordinates
        year (int): year to filter
        fire_season (boolean): include tweets only from Fire Season if true. Fire season goes
            from May to October included.
    
    Returns Plotly figure of California map with wildfires
    '''

    coord_data = filter_coord_data(coord_data, year, fire_season)

    print(coord_data)

    fig = px.choropleth_mapbox(
        coord_data, 
        geojson=coord_data.geometry.to_json(),
        locations = coord_data.index,
        color_discrete_sequence = ["red"] * coord_data.shape[0],
        mapbox_style = "stamen-terrain",
        zoom = 5, center = {'lon': -119.4179, 'lat': 36.7783},
        opacity = 0.6,
        hover_name = "fire_name",
        hover_data = ["gis_acres", "alarm_date", "cont_date"]
        )

    fig.update_layout(showlegend = False)

    return fig


'''
def map_wildfires(coord_data):

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
'''


