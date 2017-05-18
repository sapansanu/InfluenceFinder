# Trent Liu
# tliu3@mail.sfsu.edu
# 4/29/2017
#
# reads json files and returns them as user objects

import user
import json


# reads json file and returns user object
def read(file_name):
    try:
        with open(file_name, 'r') as json_data:
            info = json.load(json_data)
            read_user = user.User(info['screen_name'])
            read_user.average_retweet_count = info['average_retweet_count']
            read_user.followers_count = info['followers_count']
            read_user.influence_score = info['influence_score']
            read_user.average_favorite_count = info['average_favorite_count']
            read_user.follower_list = info['follower_list']
            return read_user
    except FileNotFoundError:
        print('Could not find file: ' + file_name)
