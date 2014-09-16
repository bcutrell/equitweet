import code # code.interact(local=locals())
from lib.panda_bro import PandaBro

panda_bro = PandaBro()

print panda_bro.get_mean_polarity()

print '********************************************'

panda_bro.normalize_polarity()

print '********************************************'

panda_bro.overall_sentiment()

print panda_bro.tweets_df