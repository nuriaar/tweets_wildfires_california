import pandas as pd
from datetime import datetime

def read_data(year, state_info = False, fire_season = False):
    '''
    Read data and filter
    '''
    if state_info:
        path = "data/twitter_data/tweets_state.csv"
    else:
        path = "data/twitter_data/sample_clean_data.csv"

    dateparse = lambda x: datetime.strptime(x, '%Y-%m-%d')

    tweets = pd.read_csv(path, parse_dates = ['Date'], date_parser = dateparse)

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
