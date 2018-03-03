from django.shortcuts import render
import os
import twitter

def index(request):
	consumerKey = os.environ["consumerKey"]
	consumerSecret = os.environ["consumerSecret"]
	accessTokenKey = os.environ["accessTokenKey"]
	accessTokenSecret = os.environ["accessTokenSecret"]
 
	api = twitter.Api(consumer_key=consumerKey,
			consumer_secret=consumerSecret,
			access_token_key=accessTokenKey,
			access_token_secret=accessTokenSecret)

	cred = api.VerifyCredentials()
	if cred is None:
		raise Exception("Could not authorize user. Please double check your credentials.")

	tweets = api.GetSearch(term="beyonce",count=100,include_entities=False, return_json=True)
	context = {"tweets":tweets}
	return render(request, "pulse/index.html", context)
