CREATE TABLE stocks (
	ticker	 varchar(8) primary key, -- name this stock?
	name  varchar(100),
	sector  varchar(100)
);
		
CREATE TABLE tweets (
	ticker   varchar(8) references stocks(ticker),
	tweet_text  varchar(140),
	polarity  double precision,
	subjectivity  double precision,
	date    date
);
