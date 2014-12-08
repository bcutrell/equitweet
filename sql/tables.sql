CREATE TABLE IF NOT EXISTS stocks (
  ticker VARCHAR(8) primary key,
  name VARCHAR(100),
  sector VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS tweets (
  ticker   VARCHAR(8) REFERENCES stocks(ticker),
  username VARCHAR(20),
  tweet_id BIGINT,
  followers_count INT,
  polarity DOUBLE PRECISION,
  subjectivity DOUBLE PRECISION,
  date DATE,
  UNIQUE (tweet_id, ticker)
);

ALTER TABLE tweets ADD COLUMN full_text VARCHAR(140);

CREATE TABLE IF NOT EXISTS prices (
  ticker VARCHAR(8) REFERENCES stocks(ticker),
  start_price REAL,
  end_price REAL,
  adj_close REAL,
  stat_date DATE
);
