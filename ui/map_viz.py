'''
Map Visualization of Wildfires
'''

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


preprocessed_data_filename = "../data/wildfire_coordinate_data/clean_wildfires_data_2019.csv"
wildfires_data = pd.read_csv(preprocessed_data_filename)

# Map
fig = go.Figure()

fig.update_layout(
    #mapbox_zoom = 6.8,
    #mapbox_center = {"lat": 41.2033 ,"lon": -77.1945},
    mapbox_style = "dark",
    margin = {"r":0, "t":0, "l":0, "b":0})

fig = go.Figure()
fig.add_trace(go.Scattermapbox(
    mode = "lines",
    lat = wildfires_data["lat"][:1000], lon = wildfires_data["lon"][:500],
    name = "Wildfire",
    marker=go.scattermapbox.Marker(size = 10, color = "gray")
    ))

fig = px.line_mapbox(wildfires_data[:500], lat="lat", lon="lon", height=300)



wildfires_data2 = wildfires_data.dropna()
fig = px.line_mapbox(wildfires_data2[:2000], lat="lat", lon="lon", color="fire_name", zoom=3)

fig.update_layout(mapbox_style="stamen-terrain", mapbox_zoom=6,
    margin={"r":0,"t":0,"l":0,"b":0})

fig.show()






fig = go.Figure(go.Scattermapbox(
    mode = "lines", fill = "toself", fillcolor = "orange",
    lon = wildfires_data["lon"],
    lat = wildfires_data["lat"],
    name = "Wildfire",
    marker=go.scattermapbox.Marker(
            color = "red", size = 10),
    text = "<b>" + wildfires_data["fire_name"] + "</b><br>" +
            "GIS Acres: " + wildfires_data["gis_acres"].astype(str) + "<br>" +
            "Alarm date: " + wildfires_data["alarm_date"] + "<br>" +
            "Contingency date: " + wildfires_data["cont_date"],
    hovertemplate = "%{text}"
    ))

fig.update_layout(
    mapbox = {'style': "stamen-terrain", 'center': {'lon': -119.4179, 'lat': 36.7783}, 'zoom': 6.5},
    showlegend = False,
    margin = {'l':0, 'r':0, 'b':0, 't':0})

fig.show()




'''
fig = px.line_mapbox(lat=wildfires_data["lat"][:500], lon=wildfires_data["lon"][:500],
                    color = wildfires_data["fire_name"][:500],
                     mapbox_style="stamen-terrain", zoom=6)

fig.update_layout(mapbox_style="stamen-terrain", mapbox_zoom=4,
    margin={"r":0,"t":0,"l":0,"b":0})

fig.show()
'''
