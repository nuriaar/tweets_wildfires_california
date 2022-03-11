'''
Utility functions
'''

import pandas as pd
import geopandas as gpd
from datetime import datetime


def is_fire_season(row):
    '''
    Return True if wildfire data row is within fire season, False otherwise.

    Inputs:
        row (Pandas Dataframe)
    '''

    if row["cont_date"].month >= 5 and row["alarm_date"].month < 11:
        return True
    else:
        return False


def filter_coord_data(coord_data, year, fire_season = False):
    '''
    Filter wildfire coordinates dataframe according to parameters.

    Inputs:
        coord_data: Pandas dataframe with coordinates
        year: (int) year to filter
        fire_season: (boolean) Include tweets only from Fire Season if true.
            Fire season goes from May to October included.
    
    Outputs:
        coord_data: Pandas dataframe with filtered data
    '''

    coord_data = coord_data[coord_data['year'] == year]
    
    if fire_season:
         coord_data = coord_data[coord_data['fire_season'] == True]

    coord_data = coord_data.reset_index()

    return coord_data


def read_coord_data():
    '''
    Read wildfire coordinate data. 
        
    Returns: 
        coord_data (Pandas Dataframe)
    '''

    data_path = "data/clean_wildfires_data.geojson"
    coord_data = gpd.read_file(data_path)

    coord_data["year"] = coord_data["year"].astype(int)

    return coord_data


def read_tweets_data(path):
    '''
    Read twitter data from path.

    Input:
        path (str)

    Returns:
        tweets (Pandas Dataframe)
    '''

    dateparse = lambda x: datetime.strptime(x, '%Y-%m-%d')
    tweets = pd.read_csv(path, parse_dates = ['Date'], date_parser = dateparse)

    return tweets


def filter_tweets_data(tweets, year, state_info = False, fire_season = False):
    '''
    Filter tweets dataframe according to parameters.

    Inputs:
        tweets: Pandas dataframe with tweets
        year: (int) year to filter
        state_info: (str) "in" for California tweets, "out" for out of state
            tweets.
            If it's false, it retrieves all tweets (including those without
            location info)
        fire_season: (boolean) Include tweets only from Fire Season if true.
            Fire season goes from May to October included.

    Outputs:
        tweets: Pandas dataframe with filtered data
    '''

    mask = (tweets['Date'].dt.year == year)
    tweets = tweets.loc[mask]

    if fire_season:
        mask_season = (tweets['Date'].dt.month >= 5) & \
                      (tweets['Date'].dt.month < 11)
        tweets = tweets[mask_season]

    if state_info:
        if state_info == "in":
            tweets = tweets.loc[tweets['State'] == 'California']
        elif state_info == "out":
            tweets = tweets.loc[tweets['State'] != 'California']
        else:
            raise TypeError("Arg State has to be 'in' or 'out'")

    return tweets
