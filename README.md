equitweet
=========

``` {.sourceCode .python}
from equitweet import init_equitweet

eqt = init_equitweet(config.TWITTER_CONFIG)

eqt.search_tweets_for_ticker('A')

eqt.batch_search_tweets_for_tickers(['A', 'B'])

eqt.write_tweets_to_file(filename='tweets.csv')
```

Next Steps
-----
- DB integration
- Backtesting, NLP, EDA examples
- Pandas support
- Luigi support
- Plotly.js Dash example

License
-------

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any means.

