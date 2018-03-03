from django.shortcuts import render
import os
import twitter


def index(request):
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

    term = 'beyonce'
    positive_score = 0
    negative_score = 0
    error = ''

    tweets = api.GetSearch(term=term, count=100, include_entities=False)

    if len(tweets) <= 0:
        error = 'No tweets could be found about ' + term + '.'
    else:
        current_folder = os.path.dirname(os.path.realpath('__file__'))
        positive_words = load_words(os.path.join(current_folder, 'pulse/sentiment-analysis/positive-words.txt'))
        negative_words = load_words(os.path.join(current_folder, 'pulse/sentiment-analysis/negative-words.txt'))

        for tweet in tweets:
            text = tweet.text.split(' ')

            for word in text:
                if word in positive_words:
                    positive_score += 1
                if word in negative_words:
                    negative_score += 1

    total_score = positive_score - negative_score
    context = {'search_term': term, 'positive_score': positive_score,
               'negative_score': negative_score, 'total_score': total_score,
               'error': error}
    return render(request, "pulse/index.html", context)


def load_words(path):
    text_file = open(path, 'r')
    lines = text_file.read().splitlines()
    return lines
