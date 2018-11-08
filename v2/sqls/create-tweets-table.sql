CREATE TABLE IF NOT EXISTS tweets (
  ticker   VARCHAR(8) REFERENCES stocks(ticker),
  username VARCHAR(20),
  full_text VARCHAR(280),
  tweet_id BIGINT,
  followers_count INT,
  polarity DOUBLE PRECISION,
  subjectivity DOUBLE PRECISION,
  date DATE,
  UNIQUE (tweet_id, ticker)
);