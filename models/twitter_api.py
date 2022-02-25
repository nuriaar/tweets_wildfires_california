'''
Pavan and Jonas

Script to get Twitter data using tweepy
'''
import tweepy
import api_access
import datetime

auth = tweepy.OAuthHandler(api_access.consumer_key, api_access.consumer_secret)
auth.set_access_token(api_access.access_token, api_access.access_token_secret)
api = tweepy.API(auth)
client = tweepy.Client(bearer_token = api_access.bearer_token)

# client = tweepy.Client(
#     consumer_key = api_access.consumer_key,
#     consumer_secret = api_access.consumer_secret,
#     access_token = api_access.access_token,
#     access_token_secret = api_access.access_token_secret
# )

tweets = tweepy.Cursor(             #geocode
    client.search_tweets,
    q = f'california wildfires',
    lang = 'en').items(10000)

#Test to see if some tweets have coordinates
for tweet in tweets:
    if tweet.place is not None:
        print(tweet.created_at)
        print(tweet.text)
        print(tweet.place)
        print('\n')