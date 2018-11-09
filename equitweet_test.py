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
        eqt = equitweet.init_equitweet(self.FAKE_CONFIG)
        assert eqt
        assert type(eqt.t) == Twitter

    def test_write_file(self):
        eqt = equitweet.init_equitweet(self.FAKE_CONFIG)
        assert eqt.NO_TWEETS_MSG == eqt.write_tweets_to_file(filename='fake.csv')

        eqt.tweets.append(self.FAKE_TWEET)
        eqt.write_tweets_to_file(filename='fake.csv')

        assert os.path.isfile('fake.csv')
        os.remove('fake.csv')

if __name__ == '__main__':
    unittest.main()
