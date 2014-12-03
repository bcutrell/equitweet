from bs4 import BeautifulSoup
from urllib2 import urlopen

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

from sklearn.feature_extraction.text  import CountVectorizer
from sklearn.feature_extraction.text  import TfidfTransformer

from collections import Counter

from nltk.corpus import stopwords as sw
from nltk.corpus import wordnet as wn

import operator

from pytagcloud import create_tag_image, make_tags
from pytagcloud.lang.counter import get_tag_counts

from pprint import pprint


def make_tag_cloud(data):
  words = ' '.join(list(data['last']))
  stop_words = sw.words()
  freqs = [(word, freq) for (word, freq) in get_tag_counts(words)
    if word not in stop_words and len(word)>2 and (can_be_noun_arg == can_be_noun(word))]
  freqs = freqs[:30]
  tags = make_tags(freqs, maxsize=80)
  fname = 'noun_last_words.png'
  create_tag_image(tags, fname, size=(900, 600), fontname='Lobster')


from string import punctuation
tweet_processed=tweet.lower()
for p in list(punctuation):
	tweet_processed=tweet_processed.replace(p,'')

import re
text = re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)


# combine all the text of a given sector

# create_tag_image(make_tags(sorted_wordscount[:],maxsize=200), 'filename.png', size=(1300,1150), background=(0, 0, 0, 255), layout=LAYOUT_MIX, fontname='Molengo', rectangular=True)


import operator
import os
import urllib2

from roundup.backends.indexer_common import STOPWORDS
import requests, collections, bs4
with open("./const11.txt") as file:
  Data1 = file.read().lower()
  Data = Data1.split()
two_words = [' '.join(ws) for ws in zip(Data, Data[1:])]
wordscount = {w:f for w, f in collections.Counter(two_words).most_common() if f > 5}
sorted_wordscount = sorted(wordscount.iteritems(), key=operator.itemgetter(1),reverse=True)

from pytagcloud import create_tag_image, create_html_data, make_tags, LAYOUT_HORIZONTAL, LAYOUTS, LAYOUT_MIX, LAYOUT_VERTICAL, LAYOUT_MOST_HORIZONTAL, LAYOUT_MOST_VERTICAL
from pytagcloud.colors import COLOR_SCHEMES
from pytagcloud.lang.counter import get_tag_counts

tags = make_tags(get_tag_counts(Data1)[:50],maxsize=260)
create_tag_image(tags,'filename.png', size=(1000,1000), background=(0, 0, 0, 255), layout=LAYOUT_MIX, fontname='Lobster', rectangular=True)`