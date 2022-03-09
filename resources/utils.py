import pandas as pd
from datetime import datetime


def filter_coord_data(coord_data, year, fire_season = False):

    coord_data = coord_data[(coord_data['year'] == year) & 
                            (coord_data['fire_season'] == fire_season)]

    return coord_data


def read_coord_data():

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
    Read data
    '''

    dateparse = lambda x: datetime.strptime(x, '%Y-%m-%d')
    tweets = pd.read_csv(path, parse_dates = ['Date'], date_parser = dateparse)
    
    return tweets


def filter_tweets_data(tweets, year, state_info = True, fire_season = True):

    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)

    mask = (tweets['Date'] >= start_date) & (tweets['Date'] <= end_date)
    tweets = tweets.loc[mask]

    if fire_season:
        mask_season = (tweets['Date'].dt.month >= 5) & (tweets['Date'].dt.month < 11)
        tweets = tweets[mask_season]
    
    if state_info:
        if state_info == "IN":
            tweets = tweets.loc[tweets['State'] == 'California']
        elif state_info == "OUT":
            tweets = tweets.loc[tweets['State'] != 'California']
        else:
            raise TypeError("State has to be IN or OUT")
    
    return tweets


