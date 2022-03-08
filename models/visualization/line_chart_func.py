'''
TO DO:
    Get rid of warnings
    Assert fire_season
    Make graph pretty
    Filter on in- or out-of-state
'''

import pandas as pd
import matplotlib.pyplot as plt
import glob



def line_chart(year, fire_season = True):
    '''
    Creates a line chart of the tweet and wildfire intensity.

    Input:
        year (int): the year
        fire_season (bool): indicating whether only the fire season is relevant
    
    Ouptput:
        line chart (plt): the plot
    '''
    assert 2015 <= year <= 2021, 'Enter a year between 2015 and 2021'                                 #### DOUBLE CHECK WITH SERGIO
    assert type(fire_season) is bool, 'fire_season must be a boolean'

    plot_data = get_plot_data(year, fire_season)
    
    fig, ax1 = plt.subplots()
    ax1.plot('week', 'acres', data = plot_data, color = 'red')
    ax2 = ax1.twinx()
    ax2.plot('week', 'nb_tweets', data = plot_data, color = 'blue')
    plt.title(f'Acres Burned and Tweet Intensity in {year}')
    ax1.set_xlabel('Week')
    ax1.set_ylabel('Burned Acres')
    ax2.set_ylabel('Number of Tweets')
    ax1.yaxis.label.set_color('red')
    ax2.yaxis.label.set_color('blue')
    plt.subplots_adjust(left = 0.15, right = 0.85, bottom = 0.15, top = 0.85)
    plt.savefig('test.png')

    return plot_data


def get_plot_data(year, fire_season):
    '''
    Gets the required data for the plot in the correct format.

    The formatting is computationally intensive and is only required
    once per year. Therefore, if it has not yet been done for a year, it saves
    the rightly-formatted dataframe. Otherwise, it simply loads the previously
    created dataframe that is in the right format.

    Input:
        year (int): the year
        fire_season (bool): indicating whether only the fire season is relevant
    
    Ouptput:
        data (pd.DataFrame): the relevant data  
    '''
    long_filenames = glob.glob('../../data/chart_data/*'.format('csv'))
    filenames = [filename.split('/')[-1] for filename in long_filenames]
    if f'{year}_plot_data.csv' in filenames:
        data = pd.read_csv(f'../../data/chart_data/{year}_plot_data.csv', index_col = 'Unnamed: 0')
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
                data.loc[week - 1, 'nb_tweets'] += 12020
    return data


def get_wildfire_data():
    '''
    Retrieves the wildfire data and puts it into the right format.

    Input:
        None
    
    Output:
        wildfire_data (pd.DataFrame): the relevant wildfire data
    '''
    wildfire_data = pd.read_csv('../../data/Cal_Fires.csv', usecols = ['YEAR_', 'STATE', 'ALARM_DATE', 'CONT_DATE', 'GIS_ACRES'])
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
    twitter_filenames = glob.glob(f'../../data/{year}*'.format('csv'))
    twitter_data = pd.concat([pd.read_csv(file, usecols = ['Date']) for file in twitter_filenames])
    twitter_data.rename(columns = {'Date': 'date'}, inplace = True)
    twitter_data['date'] = pd.to_datetime(twitter_data['date'], yearfirst = True, format = '%w', infer_datetime_format=True)
    return twitter_data
