'''
Preprocess wildfire coordinate data for map visualization
'''

import json
import pandas as pd
from datetime import datetime

import warnings
warnings.filterwarnings("ignore")

LARGE_FIRE_ACRES = 1000

json_filepath = "../data/California_Wildland_Fire_Perimeters_(All).geojson"

with open(json_filepath) as f:
    fires_gj = json.load(f)

cols = ["fire_name", "gis_acres", "year", "alarm_date", "cont_date", "lat", "lon"]
wildfires_data = pd.DataFrame(columns = cols)

years = ["2015", "2016", "2017", "2018", "2019", "2020", "2021"]

for year in years:

    i = 0
    for fire in fires_gj["features"]:
        print(i)
        i+= 1
        properties = fire["properties"]
        year = properties["YEAR_"]

        if year == year:
            gis_acres = properties["GIS_ACRES"]

            if gis_acres > LARGE_FIRE_ACRES:
                gis_acres = round(gis_acres, 4)
                fire_name = properties["FIRE_NAME"]

                alarm_date = properties["ALARM_DATE"]
                cont_date = properties["CONT_DATE"]
                if alarm_date is not None:
                    alarm_date = str(datetime.strptime(alarm_date, "%Y-%m-%dT%H:%M:%SZ").date())
                if cont_date is not None:
                    cont_date = str(datetime.strptime(cont_date, "%Y-%m-%dT%H:%M:%SZ").date())

                for polygons in fire["geometry"]["coordinates"]:

                    if isinstance(polygons[0][0], float):

                        for lon, lat in polygons:

                            # Append coordinates
                            values = [fire_name, gis_acres, year, alarm_date, cont_date, lat, lon]
                            new_row = pd.DataFrame([values], columns = cols)
                            wildfires_data = pd.concat([wildfires_data, new_row], ignore_index=True)

                        # Link back to initial coordinate
                        values = [fire_name, gis_acres, year, alarm_date, cont_date, 
                                polygons[0][1], polygons[0][0]]
                        new_row = pd.DataFrame([values], columns = cols)
                        wildfires_data = pd.concat([wildfires_data, new_row], ignore_index=True)

                        # Space between polygons
                        values = [None] * len(cols)
                        new_row = pd.DataFrame([values], columns = cols)
                        wildfires_data = pd.concat([wildfires_data, new_row], ignore_index=True)
                    
                    else:

                        for polygon in polygons:

                            for lon, lat in polygon:

                                # Append coordinates
                                values = [fire_name, gis_acres, year, alarm_date, cont_date, lat, lon]
                                new_row = pd.DataFrame([values], columns = cols)
                                wildfires_data = pd.concat([wildfires_data, new_row], ignore_index=True)
                            
                            # Link back to initial coordinate
                            values = [fire_name, gis_acres, year, alarm_date, cont_date, 
                                    polygons[0][1], polygons[0][0]]
                            new_row = pd.DataFrame([values], columns = cols)
                            wildfires_data = pd.concat([wildfires_data, new_row], ignore_index=True)

                            # Space between polygons
                            values = [None] * len(cols)
                            new_row = pd.DataFrame([values], columns = cols)
                            wildfires_data = pd.concat([wildfires_data, new_row], ignore_index=True)

    preprocessed_data_filename = "../data/wildfire_coordinate_data/clean_wildfires_data_" + year + ".csv"
    wildfires_data.to_csv(preprocessed_data_filename, index=False)
