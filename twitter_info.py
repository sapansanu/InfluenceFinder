# Trent Liu
# tliu3@mail.sfsu.edu
# 4/25/2017
#
# Grabs info using the Twitter API

import tweepy
import json

directory_to_search = '/home/trent/Documents/School/Spring 2017/CSC 877 Big Data Analysis/keys/'


def get_follower_list(u, api):
    follower_list = []
    try:
        page_collection = tweepy.Cursor(api.followers_ids, u.user_id).pages()
    except tweepy.TweepError:
        get_follower_list(authorize(1))
    for page in page_collection:
            follower_list.extend(page)

    return follower_list


def get_user_info(u):
    api = authorize()
    info = api.user_timeline(u.user_id, count=20)
    #count = 0
    for tweet in info:
        if tweet.in_reply_to_status_id is None and tweet.in_reply_to_user_id is None:
            if not hasattr(tweet, 'retweeted_status'):
                #count = count + 1
                u.retweet_count = u.retweet_count + tweet.retweet_count
                u.favorite_count = u.favorite_count + tweet.favorite_count
        u.followers = tweet.user.followers_count
    #print(count)
    return u


def get_tweet_info(tweet_id):
    api = authorize()
    tweet = api.statuses_lookup(tweet_id)
    print(tweet)
    return


def get_key(iteration, dir):
    with open(dir + str(iteration) + '.json') as key_file:
        return json.load(key_file)


def authorize(iteration):
    keys = get_key(iteration, directory_to_search)
    auth = tweepy.OAuthHandler(keys.consumer_key, keys.consumer_secret)
    auth.set_access_token(keys.access_token, keys.access_token_secret)
    return tweepy.API(auth)

