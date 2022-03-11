
import glob
import pandas as pd


def filter_plot_data(year, fire_season, data):
    '''
    Filters the data for the plot so that only the relevant year and
    weeks are taken into account.

    Input:
        year (int): the year
        fire_season (bool): indicating whether only the fire season
            is relevant
    
    Output:
        data (pd.DataFrame): the relevant plot data
    '''
    data = data.loc[year]
    if fire_season:
        data = data.loc[18:45]
    else:
        data = data.loc[0:52]
    return data.reset_index()


def get_plot_data():
    '''
    Gets the required data for the plot in the correct format.

    The formatting is computationally intensive and is only required
    once. Therefore, if it has not yet been done, it saves the
    rightly-formatted dataframe. Otherwise, it simply loads the previously
    created dataframe that is in the right format.

    Input:
        None
    
    Ouptput:
        data (pd.DataFrame): the data  
    '''
    long_filenames = glob.glob('data/*'.format('csv'))
    filenames = [filename[-13:] for filename in long_filenames]
    if 'plot_data.csv' not in filenames:
        wildfire_data = get_wildfire_data()
        twitter_data = get_twitter_data()
        data = twitter_data.groupby(['year', 'week']).count()
        data.rename(columns = {'date': 'nb_tweets'}, inplace = True)
        data['burned_acres'] = 0
        for row in wildfire_data.itertuples():
            year, start_week, end_week, acres = row[1], row[2].week, row[3].week, row[4]
            if 2015 <= year <= 2021:
                for week in range(start_week, end_week + 1):
                    data.loc[year, week].burned_acres += int(acres)
        data.to_csv(path_or_buf = 'data/plot_data.csv')
    
    data = pd.read_csv(f'data/plot_data.csv', index_col = ['year', 'week'])
    return data


def get_wildfire_data():
    '''
    Retrieves the wildfire data and puts it into the right format.

    Input:
        None
    
    Output:
        wildfire_data (pd.DataFrame): the relevant wildfire data
    '''
    wildfire_data = pd.read_csv('data/Cal_Fires.csv', usecols = ['YEAR_', 'ALARM_DATE', 'CONT_DATE', 'GIS_ACRES'])
    wildfire_data.rename(columns = {
        'YEAR_': 'year',
        'ALARM_DATE': 'alarm_date',
        'CONT_DATE': 'containment_date',
        'GIS_ACRES': 'gis_acres',
        }, inplace = True)
    wildfire_data.dropna(axis = 0, how = 'any', subset = ['year', 'alarm_date', 'containment_date', 'gis_acres'], inplace = True)
    wildfire_data['alarm_date'] = pd.to_datetime(wildfire_data['alarm_date'], yearfirst = True, format = '%w', infer_datetime_format=True)
    wildfire_data['containment_date'] = pd.to_datetime(wildfire_data['containment_date'], yearfirst = True, format = '%w', infer_datetime_format=True)
    return wildfire_data


def get_twitter_data():
    '''
    Retrieves the date (year and week) of the tweets.

    Input:
        None
    
    Output:
        twitter_data (pd.DataFrame): the relevant twitter data
    '''
    twitter_filenames = glob.glob(f'data/twitter_data/*'.format('csv'))
    twitter_data = pd.concat([pd.read_csv(file, usecols = ['Date']) for file in twitter_filenames])
    twitter_data.rename(columns = {'Date': 'date'}, inplace = True)
    twitter_data['date'] = pd.to_datetime(twitter_data['date'], yearfirst = True, format = '%w', infer_datetime_format=True)
    twitter_data['year'] = twitter_data['date'].dt.year
    twitter_data['week'] = twitter_data['date'].dt.isocalendar().week
    return twitter_data
