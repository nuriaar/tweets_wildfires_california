import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

wildfire_data = pd.read_csv('../../data/Cal_Fires.csv')
wildfire_data.rename(columns={
    'OBJECTID': 'object_id',
    'YEAR_': 'year',
    'STATE': 'state',
    'AGENCY': 'agency',
    'UNIT_ID': 'unit_id',
    'FIRE_NAME': 'fire_name',
    'INC_NUM': 'inc_num',
    'ALARM_DATE': 'alarm_date',
    'CONT_DATE': 'containment_date',
    'CAUSE': 'cause',
    'COMMENTS': 'comments',
    'REPORT_AC': 'report_ac',
    'GIS_ACRES': 'gis_acres',
    'C_METHOD': 'c_method',
    'OBJECTIVE': 'objective',
    'FIRE_NUM': 'fire_num',
    'Shape__Area': 'shape_area',
    'Shape__Length': 'shape_length'},inplace = True)
wildfire_data.dropna(axis = 0, how = 'any', subset = ['year', 'state', 'fire_name', 'alarm_date', 'containment_date', 'gis_acres', 'shape_area', 'shape_length'], inplace = True)
wildfire_data['alarm_date'] = pd.to_datetime(wildfire_data['alarm_date'], yearfirst = True, format = '%w', infer_datetime_format=True)
wildfire_data['containment_date'] = pd.to_datetime(wildfire_data['containment_date'], yearfirst = True, format = '%w', infer_datetime_format=True)

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

relevant_data = wildfire_data[wildfire_data['year'] == year].reset_index(drop = True)
relevant_data = relevant_data.loc[:, ['alarm_date', 'containment_date', 'gis_acres']]
week_dict = {'week': [week for week in range(1, 52 + 1)], 'acres': [0]*52}
data = pd.DataFrame(week_dict)
for idx, row in enumerate(relevant_data.itertuples()):
    start_week, end_week, acres = row[1].week, row[2].week, row[3]
    for week in range(start_week, end_week):
        data.loc[week - 1, 'acres'] += acres         ### gis_acres, add acres to every week burned
print(data)                 ### delete
sns.set()
x = data['week']
y = data['acres']
sns.lineplot(x = x, y = y)
plt.savefig('test.png')
plt.show()