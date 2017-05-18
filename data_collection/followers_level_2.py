#   Sapan Tiwari
#
#   Finds level 2 follower list and details

import time
import tweepy
import json
import influence_finder as finder


# Finds level 2 follower list
def find_L2_follower_list(screen_name):
    finder.get_variables()
    followers = tweepy.Cursor(finder.api.followers, screen_name=screen_name, count=200).items()
    while True:
        try:
            follower = next(followers)
        except tweepy.TweepError as e:
            print(e)
            print('RATE LIMIT - waiting 15 minute...')
            time.sleep(60*15)
            follower = next(followers)
        except StopIteration:
            break
        get_L2_follower_profile(follower, screen_name)


# Finds level 2 follower details
def get_L2_follower_profile(follower, user_screen_name):
    finder.get_variables()
    total_retweet= 0
    total_favourite = 0
    tweet_count  = 0
    follower_screen_name = follower.screen_name
    for i in range(25):
        try:
            timeline = finder.api.user_timeline(follower_screen_name, page=i, count=200)
        except tweepy.TweepError as e:
            if "Not authorized" in str(e):
                print(e)
                print("User timeline is private, Skipping...")
                return
            elif "Connection broken" in str(e):
                print(e)
                print("Trying again")
                return
            elif "Connection aborted" in str(e):
                print(e)
                print("Trying again")
                return
            else:
                print(e)
                print('RATE LIMIT - waiting 15 minute...')
                time.sleep(60*15)
                return
        for tweet in timeline:
                if (("python" in tweet.text or "Python" in tweet.text) and not tweet.retweeted):
                    print("Reading tweet : "+tweet.text)
                    total_retweet += tweet.retweet_count
                    total_favourite += tweet.favorite_count
                    tweet_count += 1
    print("Tweet count for L2 follower "+follower_screen_name+" : "+str(tweet_count))
    if tweet_count > 0:
        with open(finder.followers_L1_path+user_screen_name+".json","r") as file:
            data = json.load(file)
            data['follower_list'] += [follower_screen_name]
            finder.write_json(user_screen_name, data, finder.followers_L1_path)
        data = finder.follower_json(follower)
        average_retweet = round(total_retweet/tweet_count, 2)
        average_favourite = round(total_favourite/tweet_count, 2)
        data = finder.calculate_scores(average_retweet, average_favourite, tweet_count, data)
        finder.write_json(follower_screen_name, data, finder.followers_L2_path)
