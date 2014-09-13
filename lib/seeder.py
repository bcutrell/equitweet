import code #code.interact(local=locals())
from postgres_db import MyDB
from textblob import TextBlob
from twitter import Twitter, OAuth
## TODO: remove pandas from this file
import pandas as pd
import oauth
import json
import time, sys

############################
# STOCKS
############################
class SeedStocks(object):
    """
    For the time being this should only be run once
    """

    def __init__(self, db_config):
        self.db = MyDB(**db_config)

    def _create_temp_table(self, table_name):
        self.db.query('''
            CREATE TEMPORARY TABLE {0}
                (LIKE stocks INCLUDING INDEXES)
        '''.format(table_name))

    def run(self):
        tmp_table_name = 'tmp_stocks'
        self._create_temp_table(tmp_table_name)

        with open('data/constituents.csv', 'r') as f:
            self.db.copy_expert('''
                COPY {0}
                FROM STDIN
                DELIMITER ','
                CSV HEADER
            '''.format(tmp_table_name), f)

            # Only insert values into stocks that don't already exist
            self.db.query('''
                INSERT INTO stocks
                SELECT {0}.* FROM {0}
                LEFT JOIN stocks
                    ON stocks.ticker = {0}.ticker
                WHERE stocks.ticker IS NULL
            '''.format(tmp_table_name))

            self.db.commit()

############################
# TWEETS
############################
class SeedTweets(object):
    """
    Populates Tweets Table -- Should be Run Daily
    """

    def __init__(self, db_config):
        self.sp_data = pd.read_csv('./data/constituents.csv') # use db values instead?
        self.db = MyDB(**db_config)
        with open('./config.json', 'r') as f:
            config = json.load(f)['config']

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
        self.db.query('''
            INSERT INTO tweets (ticker, username, tweet_id, followers_count,
                polarity, subjectivity, date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (  ticker,
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
class SeedPrices(object):
    """
    Populates Prices Table -- Should be Run Daily
    """
    pass
