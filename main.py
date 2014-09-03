from lib.twitter_man import tman
from lib.postgres_db import MyDB
import lib.sentiment as senty
import numpy as np
import pandas as pd

import code 


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
