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

query = 'from:suhemparack -is:retweet'
tweets = client.search_all_tweets(query = query, max_results = 10)
for tweet in tweets.data:
    print(tweet)