
import glob
import pandas as pd

def get_plot_data(year):
    '''
    Gets the required data for the plot in the correct format.

    The formatting is computationally intensive and is only required
    once per year. Therefore, if it has not yet been done for a year, it saves
    the rightly-formatted dataframe. Otherwise, it simply loads the previously
    created dataframe that is in the right format.

    Input:
        year (int): the year
    
    Ouptput:
        data (pd.DataFrame): the relevant data  
    '''
    long_filenames = glob.glob('data/chart_data/*'.format('csv'))
    filenames = [filename[-18:] for filename in long_filenames]                   ### might run into issues because of the backslash
    if f'{year}_plot_data.csv' in filenames:                                                ### sys or path module os.path
        data = pd.read_csv(f'data/chart_data/{year}_plot_data.csv', index_col = 'Unnamed: 0')
    else:
        wildfire_data = get_wildfire_data()
        twitter_data = get_twitter_data(year)
        relevant_wildfire_data = wildfire_data[wildfire_data['year'] == year].reset_index(drop = True)                 ### filter on state as well?
        relevant_wildfire_data = relevant_wildfire_data.loc[:, ['alarm_date', 'containment_date', 'gis_acres']]
        week_dict = {'week': [week for week in range(1, 52 + 1)], 'acres': [0]*52, 'nb_tweets': [0]*52}
        data = pd.DataFrame(week_dict)
        for idx, row in enumerate(relevant_wildfire_data.itertuples()):
            start_week, end_week, acres = row[1].week, row[2].week, row[3]
            for week in range(start_week, end_week):
                data.loc[week - 1, 'acres'] += acres         ### gis_acres, add acres to every week burned
        for row in twitter_data.itertuples():
            week = row[1].week
            if 1 <= week <= 52:
                data.loc[week - 1, 'nb_tweets'] += 1
        data.to_csv(path_or_buf = f'data/chart_data/{year}_plot_data.csv')
    return data


def get_wildfire_data():
    '''
    Retrieves the wildfire data and puts it into the right format.

    Input:
        None
    
    Output:
        wildfire_data (pd.DataFrame): the relevant wildfire data
    '''
    wildfire_data = pd.read_csv('data/Cal_Fires.csv', usecols = ['YEAR_', 'STATE', 'ALARM_DATE', 'CONT_DATE', 'GIS_ACRES'])
    wildfire_data.rename(columns = {
        'YEAR_': 'year',
        'STATE': 'state',
        'ALARM_DATE': 'alarm_date',
        'CONT_DATE': 'containment_date',
        'GIS_ACRES': 'gis_acres',
        },inplace = True)
    wildfire_data.dropna(axis = 0, how = 'any', subset = ['year', 'state', 'alarm_date', 'containment_date', 'gis_acres'], inplace = True)
    wildfire_data['alarm_date'] = pd.to_datetime(wildfire_data['alarm_date'], yearfirst = True, format = '%w', infer_datetime_format=True)
    wildfire_data['containment_date'] = pd.to_datetime(wildfire_data['containment_date'], yearfirst = True, format = '%w', infer_datetime_format=True)
    return wildfire_data


def get_twitter_data(year):
    '''
    Retrieves the tweet data of the correct year and puts it into the right
    format.

    Input:
        year (bool): the year
    
    Output:
        twitter_data (pd.DataFrame): the relevant twitter data
    '''
    twitter_filenames = glob.glob(f'data/twitter_data/{year}*'.format('csv'))
    twitter_data = pd.concat([pd.read_csv(file, usecols = ['Date']) for file in twitter_filenames])
    twitter_data.rename(columns = {'Date': 'date'}, inplace = True)
    twitter_data['date'] = pd.to_datetime(twitter_data['date'], yearfirst = True, format = '%w', infer_datetime_format=True)
    return twitter_data
