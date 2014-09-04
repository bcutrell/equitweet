import code #code.interact(local=locals())
from postgres_db import MyDB
from textblob import TextBlob
from twitter import *
import pandas as pd # use pandas ystock connect if broken use ystockquote
import oauth
import json

############################
# STOCKS
############################
class SeedStocks(object):
	""" For the time being this should only be run once """
	def __init__(self):
		self.sp_data = pd.read_csv('./data/constituents.csv')
		self.db = MyDB()

	def run(self):
		for index, row in self.sp_data.iterrows():
			self.db.query("SELECT * FROM stocks WHERE ticker = %s", (row['Ticker'],))
			if self.db.fetchone() == None:
				self.db.query("INSERT INTO stocks (ticker, name, sector) VALUES (%s, %s, %s)",
				(row['Ticker'], row['Name'], row['Sector']))
			else:
				print 'Duplicate value attempt for ' + row['Ticker']
		self.db.commit()

############################
# TWEETS
############################
class SeedTweets(object):
	""" Populates Tweets Table -- Should be Run Daily """
	def __init__(self):
		self.sp_data = pd.read_csv('./data/constituents.csv') # use db values instead?
		self.db = MyDB()

		json_data=open('./config.json')
		config = json.load(json_data)['config']
		json_data.close()

		self.twitter_client = Twitter(auth=OAuth(
				config['token'],
				config['token_secret'], 
				config['consumer_key'], 
				config['consumer_secret']))

	def grab_tweets(self, ticker):
		return self.twitter_client.search.tweets(q='$' + ticker)

	def seed_tweet(self, ticker, tweet):
		self.db.query(
		"INSERT INTO tweets (	ticker, username, \
													tweet_id, tweet_text,\
			 										followers_count, polarity, \
			 										subjectivity, date)  \
		VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
		(	ticker,
			tweet['user']['name'][:15],
			tweet['id'],
			tweet['text'][:15],
			tweet['user']['followers_count'],
			TextBlob(tweet['text']).sentiment.polarity,
			TextBlob(tweet['text']).sentiment.subjectivity,
			tweet['created_at'] ))

	def run(self):
		""" max number of API requests per day: 150 """
		for index, row in self.sp_data.iterrows():
			if index == 0:
				ticker = row['Ticker']
				tweets = self.grab_tweets(ticker)
				for tweet in tweets.values()[1]:
					self.db.query("SELECT * FROM tweets WHERE tweet_id = %s", (tweet['id'],))
					if self.db.fetchone() == None:
						self.seed_tweet(ticker, tweet)
		self.db.commit()

############################
# PRICES
############################
class SeedPrices(object):
	""" Populates Prices Table -- Should be Run Daily """
	pass
	# def __init__(self):