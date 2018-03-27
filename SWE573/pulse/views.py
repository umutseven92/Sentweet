from django.shortcuts import render
from datetime import datetime, timedelta
from SWE573.pulse.helpers import twitter_helper as tw
from SWE573.pulse.helpers import sentiment_helper as sh


def index(request):
    if request.method == 'POST':

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

            tweets = tw.get_tweets(term, 50, False, new_since_str, new_until_str, 'en')

            positive, negative, neutral, compound = 0, 0, 0, 0

            for tweet in tweets:
                ss = sh.get_sentiment_scores(tweet.text)
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
                                     'neu': average_neu, 'compound': average_comp,
                                     'count': tweet_count}

        context = {'result': result}
        return render(request, "pulse/index.html", context)
    else:
        return render(request, "pulse/index.html")
