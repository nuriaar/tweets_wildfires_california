import tweepy
from resources.api_access import BEARER_TOKEN
import time
import geopy
from geopy.geocoders import Nominatim
import csv

def extract_calfire_tweets(start_date, end_date):
    '''
    Retrieve tweet data from start_date to end_date for the query 
    'wildfires california', which includes tweets with both words without
    being necessarily together.

    Inputs:
        start_date: date (str) with format 2019-01-01T00:00:00Z
        end_date: date (str) with format 2019-01-01T00:00:00Z

    Returns:
        list of responses from twitter (each response contains 500 tweets)
    '''
    client = tweepy.Client(bearer_token = BEARER_TOKEN)

    tweets = []

    for tweet in tweepy.Paginator(client.search_all_tweets,
        query = 'wildfires california', 
        start_time = start_date, 
        end_time = end_date, 
        tweet_fields = ['text', 'created_at', 'geo'], 
        place_fields = ['place_type', 'geo'],
        expansions = 'geo.place_id', 
        max_results=500):

        time.sleep(3)
        tweets.append(tweet)
    
    return tweets

def extract_tweets_info(list_of_tweet_responses, output_name):
    '''
    For a list of responses from twitter, extract important information 
    (id, date, text, and state) and write a csv file with the output name

    Inputs:
        list_of_tweet_responses: list of responses from twitter 
            (each response contains 500 tweets)
        output_name: name of csv file to write (str)

    Output:
        Writes csv file with name output_name

    '''
    location_coord = {}

    results = []

    path = "data/twitter_data/" + output_name

    # map places_ids to coordinates for all tweets
    for response in list_of_tweet_responses:
        if 'places' in response.includes.keys():
            for place in response.includes['places']:
                coordinates = place.geo['bbox']
                lat = str((coordinates[1] + coordinates[3])/ 2)
                lon = str((coordinates[0] + coordinates[2])/ 2)
                location_coord[place.id] = lat+","+lon

    # extract state information from coordinates
    location_state = map_coordinates(location_coord)

    # read list of tweet responses and extract relevant information
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
    

def map_coordinates(location_coord):
    '''
    Extract state information from coordinates (we need the coord_state intermediary
    dictionary to avoid the issue of retrieving state information for the same
    coordinates twice - which leads to an error)

    Inputs: 
        location_coord: dictionary that maps places_ids to coordinates

    Returns:
        dictionary that maps places ids to states
    '''
    geolocator = Nominatim(user_agent="geoapiExercises")

    location_state = {}
    coord_state = {}

    for key, location_str in location_coord.items():

        if not key in coord_state.keys():
            location = geolocator.reverse(location_str)

            if location is not None and 'state' in location.raw['address'].keys():
                state = location.raw['address']['state']
                coord_state[location_str] = state
                location_state[key] = state
        else:
            location_state[key] = coord_state[location_str]
    
    return location_state
