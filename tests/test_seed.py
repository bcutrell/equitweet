# https://github.com/walkermatt/python-postgres-testing-demo
from context import equitweet 
from equitweet.seeder import SeedStocks, SeedTweets

import unittest

#import code
#code.interact(local=locals())

class TestSeeder(unittest.TestCase):
  """Basic test cases."""

  def test_truth(self):
    assert True

