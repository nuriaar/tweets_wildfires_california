'''
Preprocess wildfire coordinate data for map visualization
'''

import pandas as pd
import numpy as np
import geopandas as gpd
from datetime import datetime


# Minimum level of acres to be considered a large fire
LARGE_FIRE_ACRES = 1000

# Filenames
JSON_FILEPATH = "data/California_Wildland_Fire_Perimeters_(All).geojson"
CSV_FILEPATH = "data/clean_wildfires_data.csv"


def is_fire_season(row):

    print(pd.DatetimeIndex(row["cont_date"]))

    if row["cont_date"].dt.month >= 5 and \
        row["alarm_date"].dt.month < 11:
        return True
    else:
        return False

def clean_dates(row):

    row["alarm_date"] = datetime.strptime(row["alarm_date"], "%Y-%m-%dT%H:%M:%SZ").date()
    row["cont_date"] = datetime.strptime(row["cont_date"], "%Y-%m-%dT%H:%M:%SZ").date()



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
        'gis_acres', 'geometry'], how='any')

    '''
    datetime.strptime(coord_data["alarm_date"], "%Y-%m-%dT%H:%M:%SZ").date()

    raw_coord_data["ALARM_DATE"] = coord_data["alarm_date"].apply(lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S+%Z"))

    coord_data["alarm_date"] = pd.to_datetime(raw_coord_data["ALARM_DATE"]
        ).dt.strftime("%Y-%m-%d")
    coord_data["cont_date"] = pd.to_datetime(coord_data["cont_date"]
        ).dt.strftime("%Y-%m-%d")
    coord_data["year"] = coord_data["year"].astype(int)
    

    coord_data['fire_season'] = coord_data.apply(is_fire_season, axis = 1)
    '''

    coord_data.geometry = coord_data.geometry.simplify(0.01)

    coord_data.to_csv(CSV_FILEPATH, index = False)





'''


    with open(path) as f:
        fires_gj = json.load(f)

    cols = ["fire_name", "gis_acres", "year", "alarm_date", "cont_date", "fire_season", "lat", "lon"]
    wildfires_data = pd.DataFrame(columns = cols)

    for year1 in YEARS:

        for fire in fires_gj["features"]:

            properties = fire["properties"]
            year = properties["YEAR_"]

            if year == year1:
                gis_acres = properties["GIS_ACRES"]

                if gis_acres is not None and gis_acres > LARGE_FIRE_ACRES:
                    gis_acres = round(gis_acres, 4)
                    fire_name = properties["FIRE_NAME"]

                    alarm_date = properties["ALARM_DATE"]
                    cont_date = properties["CONT_DATE"]

                    if alarm_date is not None and cont_date is not None:
                        if alarm_date is not None:
                            alarm_date = datetime.strptime(alarm_date, "%Y-%m-%dT%H:%M:%SZ").date()
                        if cont_date is not None:
                            cont_date = datetime.strptime(cont_date, "%Y-%m-%dT%H:%M:%SZ").date()
                        
                        fire_season = False
                        if cont_date.month >= 5 & alarm_date.month < 11:
                            fire_season = True

                        for polygons in fire["geometry"]["coordinates"]:

                            if isinstance(polygons[0][0], float):

                                for i, (lon, lat) in enumerate(polygons):

                                    # Take only 20% of data points for efficiency
                                    if i % 5 == 0:

                                        # Append coordinates
                                        values = [fire_name, gis_acres, year, alarm_date, cont_date, fire_season, lat, lon]
                                        new_row = pd.DataFrame([values], columns = cols)
                                        wildfires_data = pd.concat([wildfires_data, new_row], ignore_index=True)

                                # Link back to initial coordinate
                                values = [fire_name, gis_acres, year, alarm_date, cont_date, fire_season,
                                        polygons[0][1], polygons[0][0]]
                                new_row = pd.DataFrame([values], columns = cols)
                                wildfires_data = pd.concat([wildfires_data, new_row], ignore_index=True)

                                # Space between polygons
                                values = [fire_name, gis_acres, year, alarm_date, cont_date, fire_season,
                                        None, None]
                                new_row = pd.DataFrame([values], columns = cols)
                                wildfires_data = pd.concat([wildfires_data, new_row], ignore_index=True)
                            
                            else:

                                for polygon in polygons:

                                    for lon, lat in polygon:

                                        # Append coordinates
                                        values = [fire_name, gis_acres, year, alarm_date, cont_date, fire_season, lat, lon]
                                        new_row = pd.DataFrame([values], columns = cols)
                                        wildfires_data = pd.concat([wildfires_data, new_row], ignore_index=True)
                                    
                                    # Link back to initial coordinate
                                    values = [fire_name, gis_acres, year, alarm_date, cont_date, fire_season,
                                            polygons[0][1], polygons[0][0]]
                                    new_row = pd.DataFrame([values], columns = cols)
                                    wildfires_data = pd.concat([wildfires_data, new_row], ignore_index=True)

                                    # Space between polygons
                                    values = [fire_name, gis_acres, year, alarm_date, cont_date, fire_season,
                                        None, None]
                                    new_row = pd.DataFrame([values], columns = cols)
                                    wildfires_data = pd.concat([wildfires_data, new_row], ignore_index=True)

        preprocessed_data_filename = "data/wildfire_coordinate_data/clean_wildfires_data_" + year1 + ".csv"
        wildfires_data.to_csv(preprocessed_data_filename, index=False)

'''