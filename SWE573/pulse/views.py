from django.shortcuts import render
from datetime import datetime, timedelta
from .helpers import twitter_helper as tw
from .helpers import sentiment_helper as sh


def index(request):
    today = datetime.now().strftime('%Y-%m-%d')
    trend = "e.g. {0}".format(tw.get_random_trend())

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

        neg_tweet_count, pos_tweet_count, neu_tweet_count, all_tweet_count, total_comp = 0, 0, 0, 0, 0

        for d in range(delta.days + 1):
            new_since = since_date + timedelta(days=d)
            new_until = new_since + timedelta(days=1)

            new_since_str = new_since.strftime('%Y-%m-%d')
            new_until_str = new_until.strftime('%Y-%m-%d')

            tweets = tw.get_tweets(term, 100, False, new_since_str, new_until_str, 'en')

            daily_positive, daily_negative, daily_neutral, daily_compound = 0, 0, 0, 0

            for tweet in tweets:
                ss = sh.get_sentiment_scores(tweet.text)
                compound = ss['compound']
                daily_compound = daily_compound + compound
                total_comp += compound

                if compound == 0.0:
                    neu_tweet_count += 1
                elif compound > 0.0:
                    pos_tweet_count += 1
                else:
                    neg_tweet_count += 1

                daily_positive += ss['pos']
                daily_negative += ss['neg']
                daily_neutral += ss['neu']

            tweet_count = len(tweets)

            all_tweet_count += tweet_count

            if tweet_count == 0:
                average_comp = 0
                average_pos = 0
                average_neg = 0
                average_neu = 0
            else:
                average_comp = daily_compound / tweet_count
                average_pos = daily_positive / tweet_count
                average_neg = daily_negative / tweet_count
                average_neu = daily_neutral / tweet_count

            result[new_since_str] = {'pos': average_pos, 'neg': -1 * average_neg,
                                     'neu': average_neu, 'compound': average_comp,
                                     'count': tweet_count}

        pos_tweet_perc = pos_tweet_count / (all_tweet_count / 100)
        neg_tweet_perc = neg_tweet_count / (all_tweet_count / 100)
        neu_tweet_perc = neu_tweet_count / (all_tweet_count / 100)

        comp_result = total_comp / all_tweet_count

        comp_string = get_comp_result(comp_result, term)

        summary = 'Out of {0} tweets, {1} ({2:.2f}%) of them were positive, {3} ({4:.2f}%) of them were negative and ' \
                  '{5} ({6:.2f}%) of them were neutral.\n{7}'.format(all_tweet_count, pos_tweet_count, pos_tweet_perc,
                                                                     neg_tweet_count, neg_tweet_perc, neu_tweet_count,
                                                                     neu_tweet_perc, comp_string)
        context = {'result': result, 'summary': summary, 'today': today, 'trend': trend}
        return render(request, "pulse/index.html", context)
    else:
        context = {'summary': 'Please run Sentweet to get a summary.', 'today': today, 'trend':trend}
        return render(request, "pulse/index.html", context)


def get_comp_result(comp_result, term):
    if comp_result > 0.5:
        # Love
        return "To summarize, people LOVE {0}.".format(term)
    elif comp_result > 0.1:
        # Like
        return "To summarize, people LIKE {0}.".format(term)
    elif 0.1 > comp_result > -0.1:
        # Neutral
        return "To summarize, people are NEUTRAL about {0}.".format(term)
    elif comp_result < -0.1:
        # Dislike
        return "To summarize, people DISLIKE {0}.".format(term)
    elif comp_result < -0.5:
        # Hate
        return "To summarize, people HATE {0}.".format(term)
