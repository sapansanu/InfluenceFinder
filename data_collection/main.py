# Sapan Tiwari
#
# Main class handling data collection

import json
import os
import time
import tweepy
from data_collection import followers_level_1 as f1


# AUTHENTICATION (OAuth)
def authorize(authfile):
    with open(authfile, "r") as f:
        ak = f.readlines()
    f.close()
    auth1 = tweepy.auth.OAuthHandler(ak[0].replace("\n", ""), ak[1].replace("\n", ""))
    auth1.set_access_token(ak[2].replace("\n", ""), ak[3].replace("\n", ""))
    return tweepy.API(auth1)


# Searches tweets for a keyword
def search_tweets(word, c):
    for tweet in tweepy.Cursor(api.search, q=word, lang="en", count=c).items(c):
        data = {}
        data['authorid'] = tweet.author.id  # author/user ID#
        data['screen_name'] = tweet.author.screen_name
        data['followers_count'] = tweet.author.followers_count  # number of author/user followers
        data['friends_count'] = tweet.author.friends_count  # number of author/user friends
        data['verified'] = tweet.author.verified
        data['average_retweet_count'] = ""
        data['average_favorite_count'] = ""
        data['influence_score'] = ""
        data['tweet_count'] = ""
        data['follower_list'] = []
        get_user_profile(data)


# Get user details
def get_user_profile(data):
    global api, path
    total_retweet= 0
    total_favourite = 0
    tweet_count  = 0
    screen_name = data['screen_name']
    for i in range(25):
        try:
            timeline = api.user_timeline(screen_name, page=i, count=200)
        except tweepy.TweepError as e:
            if "Connection broken" in str(e):
                print(e)
                print("Trying again")
                return
            else:
                print(e)
                print('RATE LIMIT - waiting 15 minutes...')
                time.sleep(60*15)
                return
        for tweet in timeline:
                if (("python" in tweet.text or "Python" in tweet.text) and not tweet.retweeted):
                    print("Reading tweet : "+tweet.text)
                    total_retweet += tweet.retweet_count
                    total_favourite += tweet.favorite_count
                    tweet_count += 1
    print("Tweet count for "+screen_name+" : "+str(tweet_count))
    #checks if user has ever tweeted about "python"
    if tweet_count > 0:
        average_retweet = round(total_retweet/tweet_count, 2)
        average_favourite = round(total_favourite/tweet_count, 2)
        data = calculate_scores(average_retweet, average_favourite, tweet_count, data)
        write_json(screen_name, data, path)
        #finding level 1 followers
        f1.find_L1_follower_list(screen_name)
    else:
        return


# Calculates influence score
def calculate_scores(average_retweet, average_favourite, tweet_count, data):
    print("calculating score..")
    data['average_retweet_count'] = average_retweet
    data['average_favorite_count'] = average_favourite
    followers_count = data['followers_count']
    data['tweet_count'] = tweet_count
    influence_score = round((followers_count*0.5),2) + round((average_retweet*0.33),2) + round((average_favourite*0.17),2)
    data['influence_score'] = influence_score
    return data


# Writes json file
def write_json(screen_name, data, write_path):
    print("Write path :"+str(write_path))
    if not os.path.exists(write_path):
        os.makedirs(write_path)
    file = open(write_path+screen_name+".json","w")
    json.dump(data,file, indent=4)
    file.close()
    print("Writen : "+str(screen_name))


# Returns follower's json
def follower_json(follower):
    follower_data = {}
    follower_data['authorid'] = follower.id  # author/user ID#
    follower_data['screen_name'] = follower.screen_name
    follower_data['followers_count'] = follower.followers_count  # number of author/user followers
    follower_data['friends_count'] = follower.friends_count  # number of author/user friends
    follower_data['verified'] = follower.verified
    follower_data['average_retweet_count'] = ""
    follower_data['average_favorite_count'] = ""
    follower_data['influence_score'] = ""
    follower_data['tweet_count'] = ""
    follower_data['follower_list'] = []
    return follower_data


# Sets global variables
def get_variables():
    global api, path, followers_L1_path, followers_L2_path
    path = "./real_users/"
    followers_L1_path = path+"followers/"
    followers_L2_path = followers_L1_path+ "followers/"
    # OAuth key file
    authfile = './auth.k'
    api = authorize(authfile)


# MAIN ROUTINE
def main():
    global bag_of_words

    get_variables()

    bag_of_words = ['python', 'Python']

    for word in bag_of_words:
        search_tweets(word, 100)


if __name__ == "__main__":
    main()
