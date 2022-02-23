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
              fire_num INT,
              shape_area FLOAT,
              shape_length FLOAT,
              PRIMARY KEY (fire_id)
          )
          ''')

cal_fires_data = pd.read_csv(calfires_filepath)
'''
cal_fires_data['ALARM_DATE'] = pd.to_datetime(cal_fires_data['ALARM_DATE']).dt.date

rows = []
with open(calfires_filepath,'r') as file:
    csv_reader = csv.reader(file, delimiter=',')
    for row in csv_reader:
        rows.append(row)

rows[7]
cal_fires_data[cal_fires_data['ALARM_DATE'].isna()]

conn.executemany("INSERT INTO t (col1, col2) VALUES (?, ?);", to_db)


CONT_DATE,CAUSE,COMMENTS,REPORT_AC,GIS_ACRES,C_METHOD,OBJECTIVE,FIRE_NUM,Shape__Area,Shape__Length


                     
conn.commit()
conn.close()
'''