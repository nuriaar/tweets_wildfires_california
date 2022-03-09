import pandas as pd
from datetime import datetime

def read_data(year, state_info = False, fire_season = False):
    '''
    Read twitter data and filter according to parameters. 

    Inputs:
        year: (int) year to filter
        state_info: (str) "in" for California tweets, "out" for out of state tweets.
            If it's false, it retrieves all tweets (including those without location info)
        fire_season: (boolean) Include tweets only from Fire Season if true. Fire season goes
            from May to October included.
    
    Outputs:
        tweets: Pandas dataframe with filtered data
    '''
    if state_info:
        path = "data/twitter_data/tweets_state.csv"
    else:
        path = "data/twitter_data/sample_clean_data.csv"

    dateparse = lambda x: datetime.strptime(x, '%Y-%m-%d')

    tweets = pd.read_csv(path, parse_dates = ['Date'], date_parser = dateparse)

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
