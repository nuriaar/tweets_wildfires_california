'''
Map visualization of wildfires
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

    fig = px.choropleth_mapbox(
        coord_data,
        geojson = coord_data.geometry,
        locations = coord_data.index,
        color_discrete_sequence = ["red"] * coord_data.shape[0],
        mapbox_style = "stamen-terrain",
        zoom = 5,
        center = {'lon': -119.4179, 'lat': 36.7783},
        opacity = 0.6,
        hover_name = "fire_name",
        hover_data = ["gis_acres", "alarm_date", "cont_date"]
        )

    fig.update_layout(showlegend = False)

    return fig
