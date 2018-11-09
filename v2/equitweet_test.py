import unittest
import os
# import code # code.interact(local=locals())

import equitweet
from twitter import Twitter

class TestEquitweet(unittest.TestCase):

    FAKE_CONFIG = {
        "consumer_key": 'fake',
        "consumer_secret": 'fake',
        "token": 'fake',
        "token_secret": 'fake'
    }

    FAKE_TWEET = {
        'ticker': 'fake',
        'text': 'fake',
        'tweet_id': 'fake',
        'username': 'fake',
        'followers': 'fake',
        'created_date': 'fake',
        'retweet_count': 'fake',
        'favorite_count': 'fake'
    }

    def test_init_twitter(self):
        client = equitweet.init_twitter(self.FAKE_CONFIG)
        assert client
        assert type(client.t) == Twitter

    def test_write_file(self):
        client = equitweet.init_twitter(self.FAKE_CONFIG)
        assert client.NO_TWEETS_MSG == client.write_tweets_to_file(filename='fake.csv')

        client.tweets.append(self.FAKE_TWEET)
        client.write_tweets_to_file(filename='fake.csv')

        assert os.path.isfile('fake.csv')
        os.remove('fake.csv')

if __name__ == '__main__':
    unittest.main()
