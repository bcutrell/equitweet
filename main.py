## just examples for now
## this should hold python notebook steps for
## examining db
import code 
from lib.twitter_man import tman
from lib.postgres_db import MyDB
import numpy as np
import pandas as pd

# Get all S and P 500 data
sp_data = pd.read_csv('data/constituents.csv')
# sp[sp['Symbol'] == 'ABT']

# search Twitter
results = tman.search.tweets(q="$ABT")

# iter through search results
for value in results.values()[1]:
	code.interact(local=locals())
	print value['text']

# iter through s&p tickers
for sym in sp_data['Symbol']:
	print sym
