import twitter
from os import environ

twitter_api = None


def initialize():
    global twitter_api

    consumer_key = environ.get("consumerKey")
    consumer_secret = environ.get("consumerSecret")
    access_token_key = environ.get("accessTokenKey")
    access_token_secret = environ.get("accessTokenSecret")

    if not consumer_key or not consumer_secret or not access_token_key or not access_token_secret:
        raise Exception("Could not find one or more environment variables.")

    api = twitter.Api(consumer_key=consumer_key,
                      consumer_secret=consumer_secret,
                      access_token_key=access_token_key,
                      access_token_secret=access_token_secret)

    cred = api.VerifyCredentials()

    if cred is None:
        raise Exception("Could not authorize user. Please double check your credentials.")

    twitter_api = api
