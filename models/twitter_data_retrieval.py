'''
Pavan and Jonas

Script to get Twitter Data
'''
import twint
# Configure
c = twint.Config()
c.Store_json = True
c.Output = "test.json"
c.Search = "wildfires AND California"
c.Since = "2010-01-01"
c.Until = "2020-12-31"
#c.Custom["tweet"] = ["id", "date", "place", "geo", "language", "username", "tweet"]
#c.Geo = (34.052235, -118.243683, 100)
c.Limit = 10
#c.Format = "tweet: {tweet} | date: {date}"
"""
c.Format = '''date: {date} |
    time: {time} |
    place: {place} |
    tweet: {tweet} |
    language: {language} |
    retweet: {retweet} |
    near: {near} |
    geo: {geo} |
    source: {source} |
    retweet_date: {retweet_date}
    '''
"""

# Run
twint.run.Search(c)