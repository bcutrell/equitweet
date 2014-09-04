## Holds daily tasks to update DB
from lib.seeder import SeedTweets, SeedPrices

seed_tweets = SeedTweets()
seed_tweets.run()