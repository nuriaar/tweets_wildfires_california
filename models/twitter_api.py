import tweepy
import api_access
import time
import geopy
from geopy.geocoders import Nominatim
import csv

def extract_calfire_tweets(start_date, end_date):
    '''
    Format: 2019-01-01T00:00:00Z
    '''
    client = tweepy.Client(bearer_token = api_access.bearer_token)

    tweets = []

    for tweet in tweepy.Paginator(client.search_all_tweets,
        query = 'wildfires california', 
        start_time = start_date, 
        end_time = end_date, 
        tweet_fields = ['text', 'created_at', 'geo'], 
        place_fields = ['place_type', 'geo'],
        expansions = 'geo.place_id', 
        max_results=500):

        time.sleep(10)
        tweets.append(tweet)
    
    return tweets

def extract_tweets_info(list_of_tweet_responses, output_name):
    '''
    Extract and update to sql database
    '''
    location_coord = {}
    coord_state = {} #need to do this so open maps doesn't return error
    location_state = {}

    results = []
    count = 0

    path = "/home/sergiou/capp30122/proj-larry_on_fire/proj-larry_on_fire/data/" + output_name

    for response in list_of_tweet_responses:
        if 'places' in response.includes.keys():
            for place in response.includes['places']:
                coordinates = place.geo['bbox']
                lat = str((coordinates[1] + coordinates[3])/ 2)
                lon = str((coordinates[0] + coordinates[2])/ 2)
                location_coord[place.id] = lat+","+lon

    geolocator = Nominatim(user_agent="geoapiExercises")

    for key, location_str in location_coord.items():

        if not location_str in coord_state.keys():
            location = geolocator.reverse(location_str)

            if location is not None and 'state' in location.raw['address'].keys():
                state = location.raw['address']['state']
                coord_state[location_str] = state
        else:
            location_state[key] = coord_state[location_str]

    with open(path, "w") as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=",")
        spamwriter.writerow(['Id', 'Date', 'Text', 'State'])
                    
        for response in list_of_tweet_responses:       
            for tweet in response.data:
                place_id = ''
                if tweet['geo'] is not None:
                    place_id = tweet['geo']['place_id']

                tweet_id = tweet.id
                date = tweet.created_at.strftime("%Y-%m-%d")
                text = tweet.text
                state = location_state.get(place_id, None)
                spamwriter.writerow([tweet_id, date, text, state])
    