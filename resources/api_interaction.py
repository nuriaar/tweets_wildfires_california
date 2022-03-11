'''
API interaction
'''
from resources.twitter_data_retrieval import api_simulation

start_date = input('YY-MM-DD Start date?')
end_date = input('YY-MM-DD End date?')

api_simulation(start_date, end_date)