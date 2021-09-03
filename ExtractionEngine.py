from tweepy import *
import tweepy as tweepy

import csv
import re
import string
import json
import pymongo
from pymongo import MongoClient

consumer_key = "hBeGw9dboZlMTdRG0XSPsZQE2"
consumer_secret = "vScXnCqScPYj4m4Ljz53SuHvf0CtYJFVjtnspN0Z9iCQAMQFlY"
access_key = "1366648755919806465-U4yyvWzt7K2OFuZuhI7H2kEzcnaSyh"
access_secret = "gAGPmE4A3j8Y1CXjYRKOyU4NQm5ByTYkxV9wO5mNVnnPU"

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
