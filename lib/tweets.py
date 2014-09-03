import code
from postgres_db import MyDB
from twitter_man import tman
import sentiment as senty
import pandas as pd

code.interact(local=locals())

results = tman.search.tweets(q="$ABT")

db = MyDB()

for row in sp_data.iterrows():
	ticker = row['Symbol']
	tweets = tman.search.tweets(q='$' + ticker)

	for tweet in tweets.values()[1]:
		db.query(
		"INSERT INTO tweets (ticker, tweet_text, polarity, subjectibity, date)  \
		VALUES (%s, %s, %s, %s, %s)",
		(	ticker, 
			tweet['text'],
			senty.get_polarity(tweet['text']),
			senty.get_subjectivity(tweet['text']),
			tweet['created_at'] ))

db.commit()
