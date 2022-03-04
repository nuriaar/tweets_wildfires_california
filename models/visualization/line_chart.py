import pandas as pd
import matplotlib.pyplot as plt
import glob


while True:
    year = input('Enter a year (2010-2020): ')
    try:
        year = int(year)
    except:
        print('please input a valid year')
        continue
    if 2010 <= year <= 2020:
        break
    else:
        print('please enter a year within the specified range')

while True:
    season = input('Season (fire, off, both): ')
    if season in ['fire', 'off', 'both']:
        break
    else:
        print('please enter eith "fire", "off", or "both"')

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

twitter_filenames = glob.glob(f'../../data/{year}*'.format('csv'))
twitter_data = pd.concat([pd.read_csv(file, usecols = ['Date']) for file in twitter_filenames])
twitter_data.rename(columns = {'Date': 'date'}, inplace = True)
twitter_data['date'] = pd.to_datetime(twitter_data['date'], yearfirst = True, format = '%w', infer_datetime_format=True)

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

if season == 'fire':
    relevant_weeks = [w for w in range(18, 45)]
elif season == 'off':                                ### Probably take out the offseason
    relevant_weeks = [w for w in range(1, 53) if w not in range(18, 45)]
else:
    relevant_weeks = [w for w in range(1, 53)]

data = data[data['week'].isin(relevant_weeks)]
print(data)                 ### delete

fig, ax1 = plt.subplots()
ax1.plot('week', 'acres', data = data, color = 'red')
ax2 = ax1.twinx()
ax2.plot('week', 'nb_tweets', data = data, color = 'blue')
plt.title(f'Acres Burned and Tweet Intensity in {year}')
ax1.set_xlabel('Week')
ax1.set_ylabel('Burned Acres')
ax2.set_ylabel('Number of Tweets')
ax1.yaxis.label.set_color('red')
ax2.yaxis.label.set_color('blue')
plt.savefig('test.png')
