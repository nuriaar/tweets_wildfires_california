'''
Utility functions
'''

import pandas as pd
from datetime import datetime


def filter_coord_data(coord_data, year, fire_season = True):
    '''
    Filter wildfire coordinates dataframe according to parameters.

    Inputs:
        coord_data: Pandas dataframe with coordinates
        year: (int) year to filter
        fire_season: (boolean) Include tweets only from Fire Season if true. Fire season goes
            from May to October included.
    
    Outputs:
        coord_data: Pandas dataframe with filtered data
    '''

    coord_data = coord_data[(coord_data['year'] == year) & 
                            (coord_data['fire_season'] == fire_season)]

    return coord_data


def read_coord_data():
    '''
    Read wildfire coordinate data. 
        
    Returns: 
        coord_data (Pandas Dataframe)
    '''

    data_path = "data/wildfire_coordinate_data/"
    years = ["2015", "2016", "2017", "2018", "2019", "2020", "2021"]
    cols = ["fire_name", "gis_acres", "year", "alarm_date", "cont_date", "lat", "lon"]
    coord_data = pd.DataFrame(columns = cols)

    for year in years:
        coord_data_year = pd.read_csv(data_path + "clean_wildfires_data_" + year + ".csv")
        coord_data = pd.concat([coord_data, coord_data_year])
    
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


def filter_tweets_data(tweets, year, state_info = True, fire_season = True):
    '''
    Filter tweets dataframe according to parameters.

    Inputs:
        tweets: Pandas dataframe with tweets
        year: (int) year to filter
        state_info: (str) "in" for California tweets, "out" for out of state tweets.
            If it's false, it retrieves all tweets (including those without location info)
        fire_season: (boolean) Include tweets only from Fire Season if true. Fire season goes
            from May to October included.
    
    Outputs:
        tweets: Pandas dataframe with filtered data
    '''

    mask = (tweets['Date'].dt.year == year)
    tweets = tweets.loc[mask]

    if fire_season:
        mask_season = (tweets['Date'].dt.month >= 5) & (tweets['Date'].dt.month < 11)
        tweets = tweets[mask_season]
    
    if state_info:
        if state_info == "in":
            tweets = tweets.loc[tweets['State'] == 'California']
        elif state_info == "out":
            tweets = tweets.loc[tweets['State'] != 'California']
        else:
            raise TypeError("Arg State has to be 'in' or 'out'")
    
    return tweets


