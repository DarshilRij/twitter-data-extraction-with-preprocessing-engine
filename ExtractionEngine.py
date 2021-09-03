from tweepy import *
import tweepy as tweepy

import csv
import re
import string
import json
import pymongo
from pymongo import MongoClient

consumer_key = "consumer_key"
consumer_secret = "consumer_secret"
access_key = "access_key"
access_secret = "access_secret"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

jsonfile3000 = open('Tweet 3000.json', 'w')

search_words = "covid OR emergency OR immune OR vaccine OR flu OR snow"

allJSONData = []
index = 0
fileIndex = 0
collectionIndex = 1

jsonfile = None
tweetJson = {"data": []}
tweetJson3000 = {"data": []}

for tweet in tweepy.Cursor(api.search, q=search_words, count=100,
                           lang="en",
                           since_id=0).items():
    index = index+1

    print("Tweet ")
    print(index)
    if ((index % 100)) == 1:
        fileIndex += 1
        jsonfile = open('TweetFile '+str(fileIndex)+'.json', 'w')
        tweetJson = {"data": []}

    test = tweet._json

    tweetJson["data"].append(test)
    tweetJson3000["data"].append(test)

    if ((index % 100)) == 0:
        jsonfile.write(json.dumps(tweetJson))
    if index == 3000:
        jsonfile3000.write(json.dumps(tweetJson3000))
    print("\n")

    if index == 3000:
        break
