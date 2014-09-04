CREATE TABLE stocks (
	ticker	 varchar(8) primary key, -- name this stock?
	name  varchar(100),
	sector  varchar(100)
);
		
CREATE TABLE tweets (
	ticker   varchar(8) references stocks(ticker),
	username varchar(15), -- increase length
	tweet_id   bigint, -- id from twitter
	tweet_text  varchar(140), -- increase length
	followers_count  int,
	polarity    double precision,
	subjectivity    double precision,
	date    date
);

CREATE TABLE prices (
	ticker   varchar(8) references stocks(ticker),
	price 	real,
	-- what stock info do we want?
)
