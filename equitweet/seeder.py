from postgres_db import MyDB
from textblob import TextBlob
from twitter import Twitter, OAuth

import json
import re


class Seeder(object):


    def __init__(self, db_config):
        self.db = MyDB(**db_config)

    def _create_staging_table(self, table_name):
        self.db.execute('''
            CREATE TEMPORARY TABLE tmp_{0}
                (LIKE {0} INCLUDING INDEXES)
        '''.format(table_name))


############################
# STOCKS
############################
class SeedStocks(Seeder):
    """
    For the time being this should only be run once
    """

    def run(self):
        self._create_staging_table('stocks')

        with open('data/constituents.csv', 'r') as f:
            self.db.copy_expert('''
                COPY tmp_stocks
                FROM STDIN
                DELIMITER ','
                CSV HEADER
            ''', f)

            # Only insert values into stocks that don't already exist
            self.db.execute('''
                INSERT INTO stocks
                SELECT tmp_stocks.* FROM tmp_stocks
                LEFT JOIN stocks
                    ON stocks.ticker = tmp_stocks.ticker
                WHERE stocks.ticker IS NULL
            ''')


############################
# TWEETS
############################
class SeedTweets(Seeder):
    """
    Populates Tweets Table -- Should be Run Daily
    """

    def __init__(self, db_config):
        super(SeedTweets, self).__init__(db_config)

        with open('./config.json', 'r') as f:
            config = json.load(f)['config']

        self.twitter_client = Twitter(auth=OAuth(
            config['token'],
            config['token_secret'],
            config['consumer_key'],
            config['consumer_secret']))

    def _generate_query_groups(self):
        self.db.execute("SELECT ticker FROM stocks")
        sp_data = [row[0] for row in self.db.fetchall()]

        # Break into groups of 30 to keep query string below 500 chars
        groups = [{'tickers': sp_data[i:i+30]} for i in xrange(0, len(sp_data), 30)]

        for group in groups:
            group['query_string'] = ' OR '.join('$' + ticker for ticker in group['tickers'])
            group['in_clause'] = "'{0}'".format("','".join(group['tickers']))

        return groups

    def _get_twitter_rates(self):
        rate_limits = self.twitter_client.application.rate_limit_status(resources="search")['resources']['search']['/search/tweets']
        return rate_limits['reset'], rate_limits['limit'], rate_limits['remaining']

    def _make_search_request(self, query_string, max_id=None, since_id=None):
        query_args = {
            'q': query_string,
            'include_entities': False,
            'count': 100,
            'lang': 'en'
        }

        if max_id:
            query_args['max_id'] = max_id
        if since_id:
            query_args['since_id'] = since_id

        return self.twitter_client.search.tweets(**query_args)

    def _insert_tweets(self, values):
        if values:
            values_string = ','.join(values)
            self._create_staging_table('tweets')
            self.db.execute('''
                INSERT INTO tmp_tweets
                    (ticker, username, tweet_id, followers_count, polarity, subjectivity, date, full_text)
                VALUES
                    {0}
                '''.format(values_string))

            self.db.execute('''
                INSERT INTO tweets
                SELECT tmp_tweets.* FROM tmp_tweets
                LEFT JOIN tweets
                    ON tweets.ticker = tmp_tweets.ticker
                    AND tweets.tweet_id = tmp_tweets.tweet_id
                WHERE tweets.ticker IS NULL
            ''')

            self.db.execute('DROP TABLE tmp_tweets')

    def _collect_search_results(self, query_group, remaining):
        tickers = query_group['tickers']
        query_string = query_group['query_string']
        in_clause = query_group['in_clause']

        # Start where we left off
        self.db.execute('''
            SELECT MAX(tweet_id)
            FROM tweets
            WHERE ticker IN ({0})
        '''.format(in_clause))
        r = self.db.fetchone()

        since_id = r[0] if r else None
        max_id = None

        while remaining > 0:
            results = self._make_search_request(query_string, max_id=max_id, since_id=since_id)
            remaining -= 1
            since_id = None
            print('remaining: {0}').format(remaining)

            values = []
            for tweet in results['statuses']:
                text = tweet['text']
                text_blob = TextBlob(text)
                username = tweet['user']['name']
                tweet_id = tweet['id']
                followers = tweet['user']['followers_count']
                polarity = text_blob.sentiment.polarity
                subjectivity = text_blob.sentiment.subjectivity
                created_date = tweet['created_at']

                # Find all tickers mentioned by this tweet and add them to
                # the list of values to insert
                for ticker in tickers:
                    if re.search('\${0}[^A-Z]'.format(ticker), text):
                        subbed_values = self.db.mogrify(
                            '(%s, %s, %s, %s, %s, %s, %s, %s)',
                            (
                                ticker,
                                username,
                                tweet_id,
                                followers,
                                polarity,
                                subjectivity,
                                created_date,
                                text[0:140]
                            )
                        )

                        values.append(subbed_values)

            self._insert_tweets(values)

            if results['search_metadata'].get('next_results'):
                max_id = results['search_metadata']['next_results'].split('&')[0].lstrip('?max_id=')
            else:
                max_id = results['search_metadata']['max_id']
                break

        return remaining

    def run(self):
        next_reset, max_per_reset, remaining = self._get_twitter_rates()
        query_groups = self._generate_query_groups()

        for group in query_groups:
            if remaining < 1:
                print("Over the limit")
                return

            remaining = self._collect_search_results(group, remaining)


############################
# PRICES
############################
class SeedPrices(Seeder):
    """
    Populates Prices Table -- Should be Run Daily
    """
    def _get_prices(self, values):
      return
    def _insert_prices(self, values):
      return

    def run(self, tickers):
      values = self._get_prices(tickers)
      self._insert_prices(values)

