from django.shortcuts import render
from datetime import datetime, timedelta
from .helpers import twitter_helper as tw
from .helpers import sentiment_helper as sh


def index(request):
    trend = "e.g. {0}".format(tw.get_random_trend())

    if request.method == 'POST':

        term = request.POST['search_term']

        if term == '' or term is None:
            return return_error(request, 'Search term cannot be empty.', trend)

        start_date = request.POST['start_date']

        if start_date == '' or start_date is None:
            return return_error(request, 'Start date cannot be empty.', trend)

        end_date = request.POST['end_date']

        if end_date == '' or end_date is None:
            return return_error(request, 'End date cannot be empty.', trend)

        since_date = datetime.strptime(start_date, '%Y-%m-%d')
        until_date = datetime.strptime(end_date, '%Y-%m-%d')

        if until_date > datetime.now():
            return return_error(request, 'End date cannot be a future date.', trend)

        if since_date > until_date:
            return return_error(request, 'End date cannot be older than start date.', trend)

        delta = until_date - since_date

        result = {}

        neg_tweet_count, pos_tweet_count, neu_tweet_count, all_tweet_count, total_comp = 0, 0, 0, 0, 0

        for d in range(delta.days + 1):
            new_since = since_date + timedelta(days=d)
            new_until = new_since + timedelta(days=1)

            new_since_str = new_since.strftime('%Y-%m-%d')
            new_until_str = new_until.strftime('%Y-%m-%d')

            tweets = tw.get_tweets(term, 100, False, new_since_str, new_until_str, 'en')

            tweet_texts = [t.text for t in tweets]

            sent_info = sh.get_sentiment_info(tweet_texts)
            misc_info = sent_info[1]
            neg_tweet_count += misc_info['neg_tweet_count']
            pos_tweet_count += misc_info['pos_tweet_count']
            neu_tweet_count += misc_info['neu_tweet_count']
            all_tweet_count += misc_info['all_tweet_count']
            total_comp += misc_info['total_comp']

            result[new_since_str] = sent_info[0]

        if all_tweet_count == 0:
            return return_error(request, 'No tweets containing {0} are found.'.format(term), trend)

        pos_tweet_perc = pos_tweet_count / (all_tweet_count / 100)
        neg_tweet_perc = neg_tweet_count / (all_tweet_count / 100)
        neu_tweet_perc = neu_tweet_count / (all_tweet_count / 100)

        comp_result = total_comp / all_tweet_count

        comp_string = get_comp_result(comp_result, term)

        summary = 'Out of {0} tweets, {1} ({2:.2f}%) of them were positive, {3} ({4:.2f}%) of them were negative and ' \
                  '{5} ({6:.2f}%) of them were neutral.\n{7}'.format(all_tweet_count, pos_tweet_count, pos_tweet_perc,
                                                                     neg_tweet_count, neg_tweet_perc, neu_tweet_count,
                                                                     neu_tweet_perc, comp_string)
        context = {'result': result, 'summary': summary, 'trend': trend}
        return render(request, "pulse/index.html", context)
    else:
        context = {'summary': 'Please run Sentweet to get a summary.', 'trend': trend}
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

def return_error(request, error_string, trend):
        context = {'summary': 'Please run Sentweet to get a summary.', 'trend': trend,'error_string':error_string}
        return render(request, "pulse/index.html", context)