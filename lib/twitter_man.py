from twitter import *
import oauth
import json

json_data=open('./config.json')
config = json.load(json_data)['config']
json_data.close()

tman = Twitter(auth=OAuth(config['token'], config['token_secret'], config['consumer_key'], config['consumer_secret']))
