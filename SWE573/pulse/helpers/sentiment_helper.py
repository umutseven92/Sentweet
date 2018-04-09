from nltk.sentiment.vader import SentimentIntensityAnalyzer


def get_sentiment_scores(body):
    sid = SentimentIntensityAnalyzer()
    ss = sid.polarity_scores(body)
    return ss


def get_sentiment_info(tweets):
    daily_positive, daily_negative, daily_neutral, daily_compound = 0, 0, 0, 0

    neg_tweet_count, pos_tweet_count, neu_tweet_count, all_tweet_count, total_comp = 0, 0, 0, 0, 0

    for tweet in tweets:
        ss = get_sentiment_scores(tweet)
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

    result = {'pos': average_pos, 'neg': -1 * average_neg,
              'neu': average_neu, 'compound': average_comp,
              'count': tweet_count}

    misc = {'neg_tweet_count': neg_tweet_count, 'pos_tweet_count': pos_tweet_count, 'neu_tweet_count': neu_tweet_count,
            'all_tweet_count': all_tweet_count, 'total_comp': total_comp}

    return result, misc
