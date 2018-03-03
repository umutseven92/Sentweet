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

    tweets = api.GetSearch(term="beyonce", count=100, include_entities=False, return_json=True)
    context = {"tweets": tweets}
    return render(request, "pulse/index.html", context)
