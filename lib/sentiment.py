from textblob import TextBlob

def get_polarity(text):
	return TextBlob(text).sentiment.polarity

def get_subjectivity(text):
	return TextBlob(text).sentiment.subjectivity
