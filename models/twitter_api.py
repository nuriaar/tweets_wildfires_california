'''
Pavan and Jonas

Script to get Twitter data using tweepy
'''
import tweepy
import api_access

auth = tweepy.OAuthHandler(api_access.consumer_key, api_access.consumer_secret)
auth.set_access_token(api_access.access_token, api_access.access_token_secret)

api = tweepy.API(auth)

client = tweepy.Client(bearer_token = api_access.bearer_token)

# tweets = client.search_all_tweets(
#     query = 'california wildfires',
#     max_results = 10)
# for tweet in tweets.data:
#     print(tweet)
#     print('\n')

# date, coordinates, text

#Get the tweets
tweets = tweepy.Cursor(             #geocode
    api.search_tweets,
    q = 'california wildfires',
    lang = 'en').items(100000)

#Test to see if some tweets have coordinates
for tweet in tweets:
    if tweet.coordinates != None:
        print(tweet.coordinates)