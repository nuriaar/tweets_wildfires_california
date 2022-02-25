'''
Pavan and Jonas

Script to get Twitter data using twint
'''
import twint
# Configure
c = twint.Config()
#c.Location = True
c.Store_json = True
c.Output = "test.json"
c.Search = "wildfires AND California"
#c.Since = "2010-01-01"
#c.Until = "2020-12-31"
c.Custom['id', 'date', 'time', 'place', 'tweet', 'geo', 'language', 'retweet', 'near', 'geo', 'source', 'retweet_date'] = ['id', 'date', 'time', 'place', 'tweet', 'geo', 'language', 'retweet', 'near', 'geo', 'source', 'retweet_date']
#c.Geo = (34.052235, -118.243683, 100)
c.Limit = 1000

# Run
twint.run.Search(c)