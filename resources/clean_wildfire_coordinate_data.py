'''
Preprocess wildfire coordinate data for map visualization
'''

import json
import pandas as pd
from datetime import datetime


# Minimum level of acres to be considered a large fire
LARGE_FIRE_ACRES = 1000

json_filepath = "data/California_Wildland_Fire_Perimeters_(All).geojson"
YEARS = ["2015", "2016", "2017", "2018", "2019", "2020", "2021"]

def preprocess_wildfire_coord_data(path):
    '''
    Create csv files with wildfire coordinate data from geojson file to input
    map visualization.

    Input:
        path (string): json filepath
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

