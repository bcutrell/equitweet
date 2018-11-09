CREATE TABLE IF NOT EXISTS prices (
  ticker VARCHAR(8) REFERENCES stocks(ticker),
  start_price REAL,
  end_price REAL,
  adj_close REAL,
  stat_date DATE
);
