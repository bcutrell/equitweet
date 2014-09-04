## Twitter Debugging
# import code code.interact(local=locals())
from twitter import *
import oauth
import json

json_data=open('./config.json')
config = json.load(json_data)['config']
json_data.close()

tman = Twitter(auth=OAuth(config['token'], config['token_secret'], config['consumer_key'], config['consumer_secret']))

# search Twitter
# results = tman.search.tweets(q="$ABT")

# find tweet by id
# tman.statuses.show(_id=507517996634738688)