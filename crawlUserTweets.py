__author__ = 'ellfae'

import requests
import json
import urllib
import sys
import os
import codecs
import json
import csv
from twython import Twython
import time

## To keep track of the last tweet obtained
def getLastTweet(uid, t):
	user_timeline = t.get_user_timeline(user_id=uid,count=1)
	return (user_timeline[0]["id"])

## Retrieve user tweets - Limit: 3000 tweets
def getTweets(user_id):
	
	consumer_key = "***** YOUR KEY *****"
	consumer_secret ="**** YOUR SECRET *****"
	access_token ="**** YOUR ACCESS TOKEN *****"
	access_token_secret ="**** YOUR ACCESS TOKEN SECRET *****"
	twitter = Twython(consumer_key, consumer_secret,access_token,access_token_secret )

	tweetCount = 0
	lis = []
	lis.append(getLastTweet(user_id,twitter))
	
	for i in range(0, 16): #iterate through all tweets
	## tweet extract method with the last list item as the max_id
		user_timeline = twitter.get_user_timeline(user_id=user_id,count=200, include_retweets=False, max_id=lis[-1])
		time.sleep(300) ## 5 minute rest between api calls

		for tweet in user_timeline:
			tweetCount+=1
			print tweet['text'] ## You can store the tweet in a list and return it
			lis.append(tweet['id']) ## append tweet id's

	return tweetCount

#*********************************
#MAIN PROGRAM

#Tweet event with userid parameter and return the number of tweets obtained so far
tweets = getTweets('user-id')

print (tweets)