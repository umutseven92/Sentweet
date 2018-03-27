from django.shortcuts import render
from datetime import datetime, timedelta
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from django.http import Http404
from os import environ
import twitter


def index(request):

    if request.method == 'POST':
        # If env not found, no exceptions will be thrown.
        consumer_key = environ.get("consumerKey")
        consumer_secret = environ.get("consumerSecret")
        access_token_key = environ.get("accessTokenKey")
        access_token_secret = environ.get("accessTokenSecret")
        
        # Manuel handling of env exception.
        if not consumer_key or not consumer_secret or not access_token_key or not access_token_secret:
            # Change this to an actual error page.
            return Http404
        api = twitter.Api(consumer_key=consumer_key,
                          consumer_secret=consumer_secret,
                          access_token_key=access_token_key,
                          access_token_secret=access_token_secret)

        cred = api.VerifyCredentials()

        if cred is None:
            raise Exception("Could not authorize user. Please double check your credentials.")

        term = request.POST['search_term']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']

        since_date = datetime.strptime(start_date, '%Y-%m-%d')
        until_date = datetime.strptime(end_date, '%Y-%m-%d')

        delta = until_date - since_date

        result = {}
        for d in range(delta.days):
            new_since = since_date + timedelta(days=d)
            new_until = new_since + timedelta(days=1)

            new_since_str = new_since.strftime('%Y-%m-%d')
            new_until_str = new_until.strftime('%Y-%m-%d')
            tweets = api.GetSearch(term=term, count=50, include_entities=False,
                                   since=new_since_str, until=new_until_str,
                                   lang='en')

            positive, negative, neutral, compound = 0, 0, 0, 0

            for tweet in tweets:
                tweet_body = tweet.text
                sid = SentimentIntensityAnalyzer()
                ss = sid.polarity_scores(tweet_body)
                compound = compound + ss['compound']
                positive = positive + ss['pos']
                negative = negative + ss['neg']
                neutral = neutral + ss['neu']

            tweet_count = len(tweets)

            if tweet_count == 0:
                average_comp = 0
                average_pos = 0
                average_neg = 0
                average_neu = 0
            else:
                average_comp = compound / tweet_count
                average_pos = positive / tweet_count
                average_neg = negative / tweet_count
                average_neu = neutral / tweet_count

            result[new_since_str] = {'pos': average_pos, 'neg': average_neg,
                                     'neu': average_neu, 'compound': average_comp}

        context = {'result': result}
        return render(request, "pulse/index.html", context)
    else:
        return render(request, "pulse/index.html")
