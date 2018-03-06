from django.shortcuts import render
from datetime import datetime, timedelta
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os
import twitter


def index(request):

    if request.method == 'POST':
        consumer_key = os.environ["consumerKey"]
        consumer_secret = os.environ["consumerSecret"]
        access_token_key = os.environ["accessTokenKey"]
        access_token_secret = os.environ["accessTokenSecret"]

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
            tweets = api.GetSearch(term=term, count=100, include_entities=False, since=new_since_str, until=new_until_str,
                                   lang='en')
            compound = 0
            for tweet in tweets:
                tweet_body = tweet.text
                sid = SentimentIntensityAnalyzer()
                ss = sid.polarity_scores(tweet_body)
                comp = ss['compound']
                compound = compound + comp

            average_comp = compound / len(tweets)
            result[new_since_str] = average_comp

        context = {'result': result}
        return render(request, "pulse/index.html", context)
    else:
        return render(request, "pulse/index.html")
