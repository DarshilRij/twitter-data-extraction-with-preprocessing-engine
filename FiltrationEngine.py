from tweepy import *
import tweepy as tweepy

import pandas as pd
import csv
import re
import string
import json
import pymongo
from pymongo import MongoClient

jsonfile = open('Tweet 3000.json')

jsondata = json.load(jsonfile)

myclient = pymongo.MongoClient("key")
mydb = myclient['TweetDB']
mycollection = mydb["TweetCollection"]


print("Mongo DB Connection Success")

index = 0
collectionIndex = 1

regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"
                               u"\U0001F300-\U0001F5FF"
                               u"\U0001F680-\U0001F6FF"
                               u"\U0001F1E0-\U0001F1FF"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)


def removeUnnecessaryKV(tweet):
    for key, value in dict(tweet).items():
        if "truncated" == key:
            del tweet["truncated"]
        if "entities" == key:
            del tweet["entities"]
        if "extended_entities" == key:
            del tweet["extended_entities"]
        if "is_quote_status" == key:
            del tweet["is_quote_status"]
        if "favorited" == key:
            del tweet["favorited"]
        if "retweeted" == key:
            del tweet["retweeted"]
        if "possibly_sensitive" == key:
            del tweet["possibly_sensitive"]
    return tweet


def removeNull(tweet, key, value):
    if value is None:
        del tweet[key]


def filterTweets(tweet):
    for key, value in dict(tweet).items():
        if key == "text":
            tweet[key] = re.sub(regex, " ", value)
        if isinstance(value, str):
            if re.findall(regex, value) and key != "text":
                del tweet[key]
        if key == "user":
            for keyuser, valueuser in dict(tweet[key]).items():
                if isinstance(valueuser, str):
                    if re.findall(regex, valueuser):
                        del tweet[key][keyuser]
                removeNull(tweet[key], keyuser, valueuser)
                # if valueuser is None:
                #     del tweet[key][keyuser]

        if key == "retweeted_status":

            for keyretweet, valueretweet in dict(tweet[key]).items():
                tweet[key] = removeUnnecessaryKV(tweet[key])

            for keyretweet, valueretweet in dict(tweet[key]).items():

                if isinstance(valueretweet, str):
                    if re.findall(regex, valueretweet):
                        del tweet[key][keyretweet]
                if valueretweet is None:
                    del tweet[key][keyretweet]
                if keyretweet == "user":
                    for keyuser, valueuser in dict(tweet[key][keyretweet]).items():
                        if isinstance(valueuser, str):
                            if re.findall(regex, valueuser):
                                del tweet[key][keyretweet][keyuser]
                        removeNull(tweet[key][keyretweet], keyuser, valueuser)

        removeNull(tweet, key, value)

    for key in dict(tweet):
        if "text" in tweet:
            tweet["text"] = remove_emoji(tweet["text"])
            tweet["text"] = re.sub('[^A-Za-z0-9]+', ' ', tweet["text"])
        if "retweeted_status" in tweet:
            if "text" in tweet["retweeted_status"]:
                tweet["retweeted_status"]["text"] = remove_emoji(
                    tweet["retweeted_status"]["text"])
                tweet["retweeted_status"]["text"] = re.sub(
                    '[^A-Za-z0-9]+', ' ', tweet["retweeted_status"]["text"])

        if "user" in tweet:
            if "name" in tweet["user"]:
                tweet["user"]["name"] = remove_emoji(tweet["user"]["name"])
            if "location" in tweet["user"]:
                tweet["user"]["location"] = remove_emoji(tweet["user"]["location"])
            if "description" in tweet["user"]:
                tweet["user"]["description"] = remove_emoji(
                    tweet["user"]["description"])

    return tweet


for tweet in jsondata['data']:

    tweet = removeUnnecessaryKV(tweet)

    filterTweets(tweet)

    x = mycollection.insert_one(tweet)

print("Tweets Filtered Successful and stored in MongoDB")
