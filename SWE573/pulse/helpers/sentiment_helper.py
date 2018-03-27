from nltk.sentiment.vader import SentimentIntensityAnalyzer


def get_sentiment_scores(body):
    sid = SentimentIntensityAnalyzer()
    ss = sid.polarity_scores(body)
    return ss
