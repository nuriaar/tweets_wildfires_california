import sqlite3
import csv
import datetime
import pandas as pd

calfires_filepath = '../data/Cal_Fires.csv'

db_filepath = '../data/larry_on_fire.sqlite'
sqlite3.connect(db_filepath)

# Create tweets table
conn = sqlite3.connect(db_filepath) 
c = conn.cursor()

c.execute('''
          CREATE TABLE IF NOT EXISTS tweets (
              tweet_id INT NOT NULL,
              date DATE FORMAT 'yyyy-mm-dd',
              tweet VARCHAR(350),
              location VARCHAR(50),
              PRIMARY KEY (tweet_id)
          )
          ''')
                     
conn.commit()
conn.close()

# Insert tweet to tweets table
conn = sqlite3.connect(db_filepath) 
c = conn.cursor()

insert_query = '''
                    INSERT INTO tweets (tweet_id, date, tweet, location)
                        VALUES (?, ?, ?, ?)
                '''

args = [1, "2020-01-01", "lasdhglñsghd", "CA"]
c.execute(insert_query, args)

conn.commit()
conn.close()


# Create cal_fires table
conn = sqlite3.connect(db_filepath) 
c = conn.cursor()

c.execute('''
          CREATE TABLE IF NOT EXISTS cal_fires (
              fire_id INT NOT NULL,
              year INT NOT NULL,
              state VARCHAR(10),
              agency VARCHAR(10),
              unit_id VARCHAR(10),
              fire_name VARCHAR(50),
              inc_num INT,
              alarm_date DATE FORMAT 'yyyy-mm-dd',
              cont_date DATE FORMAT 'yyyy-mm-dd',
              cause VARCHAR(50),
              comments VARCHAR(100),
              report_ac VARCHAR(100),
              gis_acres FLOAT,
              c_method INT,
              objective VARCHAR(100),
              fire_num INT,
              shape_area FLOAT,
              shape_length FLOAT,
              PRIMARY KEY (fire_id)
          )
          ''')

cal_fires_data = pd.read_csv(calfires_filepath)
cal_fires_data['ALARM_DATE'] = str(pd.to_datetime(cal_fires_data['ALARM_DATE']).dt.date)
cal_fires_data['CONT_DATE'] = str(pd.to_datetime(cal_fires_data['ALARM_DATE']).dt.date)

fires_insert_q = '''
    INSERT INTO cal_fires (fire_id, year, state, agency, unit_id, fire_name,
        inc_num, alarm_date, cont_date, cause, comments, report_ac, gis_acres,
        c_method, objective, fire_num, shape_area, shape_length)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''

for args in cal_fires_data.values.tolist():
    conn = sqlite3.connect(db_filepath) 
    c = conn.cursor()
    c.execute(fires_insert_q, args)
    c.close()
    conn.commit
                     
conn.commit()
conn.close()
