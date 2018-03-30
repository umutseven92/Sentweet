from django.shortcuts import render
from datetime import datetime, timedelta
from .helpers import twitter_helper as tw
from .helpers import sentiment_helper as sh


def index(request):
    today = datetime.now().strftime('%Y-%m-%d')

    if request.method == 'POST':

        term = request.POST['search_term']

        if term == '' or term is None:
            context = {'error': 'Search term cannot be empty.'}
            return render(request, "pulse/index.html", context)

        start_date = request.POST['start_date']

        if start_date == '' or start_date is None:
            context = {'error': 'Start date cannot be empty.'}
            return render(request, "pulse/index.html", context)

        end_date = request.POST['end_date']

        if end_date == '' or end_date is None:
            context = {'error': 'End date cannot be empty.'}
            return render(request, "pulse/index.html", context)

        since_date = datetime.strptime(start_date, '%Y-%m-%d')
        until_date = datetime.strptime(end_date, '%Y-%m-%d')

        if until_date > datetime.now():
            context = {'error': 'End date cannot be a future date.'}
            return render(request, "pulse/index.html", context)

        if since_date > until_date:
            context = {'error': 'End date cannot be older than start date.'}
            return render(request, "pulse/index.html", context)

        delta = until_date - since_date

        result = {}

        neg_tweet_count, pos_tweet_count, neu_tweet_count, all_tweet_count = 0, 0, 0, 0

        for d in range(delta.days + 1):
            new_since = since_date + timedelta(days=d)
            new_until = new_since + timedelta(days=1)

            new_since_str = new_since.strftime('%Y-%m-%d')
            new_until_str = new_until.strftime('%Y-%m-%d')

            tweets = tw.get_tweets(term, 100, False, new_since_str, new_until_str, 'en')

            positive, negative, neutral, compound = 0, 0, 0, 0

            for tweet in tweets:
                ss = sh.get_sentiment_scores(tweet.text)
                compound = compound + ss['compound']

                if compound == 0.0:
                    neu_tweet_count += 1
                elif compound > 0.0:
                    pos_tweet_count += 1
                else:
                    neg_tweet_count += 1

                positive = positive + ss['pos']
                negative = negative + ss['neg']
                neutral = neutral + ss['neu']

            tweet_count = len(tweets)

            all_tweet_count += tweet_count

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

            result[new_since_str] = {'pos': average_pos, 'neg': -1 * average_neg,
                                     'neu': average_neu, 'compound': average_comp,
                                     'count': tweet_count}

        summary = 'Out of {} tweets, {} ({}%) of them were positive, {} ({}%) of them were negative and {} ({}%) of them were neutral.'.format(
            all_tweet_count, pos_tweet_count, pos_tweet_count / (all_tweet_count/100), neg_tweet_count, neg_tweet_count / (all_tweet_count/100),
            neu_tweet_count, neu_tweet_count / (all_tweet_count/100))
        context = {'result': result, 'summary': summary, 'today': today}
        return render(request, "pulse/index.html", context)
    else:
        context = {'summary': 'Please run Sentweet to get a summary.', 'today': today}
        return render(request, "pulse/index.html", context)
