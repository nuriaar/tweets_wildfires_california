'''
Preprocess wildfire coordinate data for map visualization
'''

import pandas as pd
import geopandas as gpd
from datetime import datetime

from resources.utils import is_fire_season


# Minimum level of acres to be considered a large fire
LARGE_FIRE_ACRES = 1000

# Filenames
JSON_FILEPATH = "data/California_Wildland_Fire_Perimeters_(All).geojson"
NEW_JSON_FILEPATH = "data/clean_wildfires_data.geojson"


def preprocess_wildfire_coord_data():
    '''
    Create csv file with wildfire coordinate data from geojson file to input
    map visualization.
    '''

    raw_coord_data = gpd.read_file(JSON_FILEPATH)

    cols = ['OBJECTID', 'YEAR_', 'AGENCY', 'FIRE_NAME', 'ALARM_DATE',
        'CONT_DATE', 'CAUSE','GIS_ACRES', 'Shape__Area', 'Shape__Length',
        'geometry']
    coord_data = raw_coord_data[cols]

    coord_data.rename(columns={'OBJECTID': 'object_id', 'YEAR_': 'year',
        'AGENCY': 'agency', 'FIRE_NAME': 'fire_name', 
        'ALARM_DATE': 'alarm_date', 'CONT_DATE': 'cont_date', 'CAUSE': 'cause',
        'GIS_ACRES': 'gis_acres', 'Shape__Area': 'shape_area', 
        'Shape__Length': 'shape_length'}, inplace = True)

    coord_data = coord_data[coord_data["gis_acres"] > LARGE_FIRE_ACRES]
    coord_data = coord_data.dropna(subset = ['year', 'alarm_date', 'cont_date',
        'gis_acres', 'geometry'], how = 'any')

    coord_data["alarm_date"] = pd.to_datetime(coord_data["alarm_date"], 
        errors = 'coerce').dt.strftime("%Y-%m-%d")
    coord_data["alarm_date"] = coord_data["alarm_date"].apply( \
        lambda x: datetime.strptime(x, "%Y-%m-%d"))

    coord_data["cont_date"] = pd.to_datetime(coord_data["cont_date"],
        errors = 'coerce').dt.strftime("%Y-%m-%d")
    coord_data["cont_date"] = coord_data["cont_date"].apply( \
        lambda x: datetime.strptime(x, "%Y-%m-%d"))

    coord_data['fire_season'] = coord_data.apply(is_fire_season, axis = 1)

    coord_data.geometry = coord_data.geometry.simplify(0.01)

    coord_data.to_file(NEW_JSON_FILEPATH, driver='GeoJSON')
