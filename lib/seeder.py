# import code #code.interact(local=locals())
from postgres_db import MyDB
from textblob import TextBlob
from twitter import *
import pandas as pd # use pandas ystock connect if broken use ystockquote
import time, sys, oauth, json

class Seeder(object):
	def __init__(self):
		self.sp_data = pd.read_csv('./data/constituents.csv')
		self.db = MyDB()

############################
# STOCKS
############################
class SeedStocks(Seeder):
	""" For the time being this should only be run once """
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
class SeedTweets(Seeder):
	""" Populates Tweets Table -- Should be Run Daily """
	def __init__(self):
		json_data=open('./config.json')
		config = json.load(json_data)['config']
		json_data.close()
		self.twitter_client = Twitter(auth=OAuth(
				config['token'],
				config['token_secret'], 
				config['consumer_key'], 
				config['consumer_secret']))

	def get_twitter_rates(self):
		rate_limits = self.twitter_client.application.rate_limit_status(resources="search")['resources']['search']['/search/tweets']
		return rate_limits['reset'], rate_limits['limit'], rate_limits['remaining']

	def grab_tweets(self, ticker, twitter_rates):
		try:
			next_reset, max_per_reset, remaining = twitter_rates
		except:
			print "ERROR:" + "Connecting to Twitter API via OAuth2 sign, could not get rate limits"
			sys.exit(1)
		while True:
			if time.time() > next_reset:
				try:
					next_reset, _, remaining = self.get_twitter_rates()
				except:
					next_reset += 15*60
					remaining = max_per_reset
			if not remaining:
				# log("WARNING", "Stalling search queries with rate exceeded for the next %s seconds" % max(0, int(next_reset - time.time())))
				time.sleep(1 + max(0, next_reset - time.time()))
				continue
			while remaining:
				try:
					return self.twitter_client.search.tweets(q='$' + ticker)
				except:
					# log("WARNING", "Search connection could not be established, retrying in 2 secs (%s: %s)" % (type(e), e))
					time.sleep(2)
					continue

	def seed_tweet(self, ticker, tweet):
		self.db.query(
		"INSERT INTO tweets (	ticker, username, \
													tweet_id, \
			 										followers_count, polarity, \
			 										subjectivity, date)  \
		VALUES (%s, %s, %s, %s, %s, %s, %s)",
		(	ticker,
			tweet['user']['name'],
			tweet['id'],
			tweet['user']['followers_count'],
			TextBlob(tweet['text']).sentiment.polarity,
			TextBlob(tweet['text']).sentiment.subjectivity,
			tweet['created_at'] ))

	def run(self):
		twitter_rates = self.get_twitter_rates()
		for index, row in self.sp_data.iterrows():
			ticker = row['Ticker']
			tweets = self.grab_tweets(ticker, twitter_rates)
			for tweet in tweets.values()[1]:
				self.db.query("SELECT * FROM tweets WHERE tweet_id = %s", (tweet['id'],))
				if self.db.fetchone() == None:
					self.seed_tweet(ticker, tweet)
					self.db.commit()

############################
# PRICES
############################
class SeedPrices(Seeder):
	""" Populates Prices Table -- Should be Run Daily """
	pass