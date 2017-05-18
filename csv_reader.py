# Trent Liu
# tliu3@mail.sfsu.edu
# 4/29/2017
#
# runs through specified directory and compiles user information

import os
import user
import json
import csv

# iterate through files in the directory to compile user information
def sort(search_dir, out_dir):
    for file_name in os.listdir(search_dir):
        # try to open files in the directory
        try:
            if file_name != 'Counts.csv' and file_name != 'Politics.csv':
                with open(search_dir + file_name, 'rt') as csvfile:
                    name = file_name.split(".")[0]
                    csvreader = csv.reader(csvfile, delimiter=',')
                    new_user = user.User(name)
                    retweet_count = 0
                    favorite_count = 0

                    # iterate through csv lines and compile information
                    for row in csvreader:
                        retweet_count += int(row[0])
                        favorite_count += int(row[1])
                    new_user.retweet_count = retweet_count
                    new_user.favorite_count = favorite_count
                    get_followers(new_user, search_dir)
                    temp = new_user.to_json()

                    # try to write JSON file
                    try:
                        with open(out_dir + name + '.json', 'w+') as outfile:
                            json.dump(temp, outfile)
                    except Exception:
                        print('Could not write file')
        except FileNotFoundError:
            print("File not found")

# reads the compiled Counts.csv folder and adjusts the values of the user attributes
def get_followers(user, search_dir):
    with open(search_dir + 'Counts.csv') as infile:
        for line in infile:
            tokens = line.split(',')

            # if matching user_id, then change attributes
            if tokens[0] is user.user_id:
                user.average_retweet_count = float(tokens[1])
                user.average_favorite_count = float(tokens[2])
                user.followers = int(tokens[3])
                user.verified = bool(tokens[4])
                break



# reads json files and returns a dictionary full of users
def read(search_dir):
    user_dict = {}
    for file_name in os.listdir(search_dir):
        try:
            with open(search_dir+file_name, 'r') as json_data:
                info = json.load(json_data)
                read_user = user.User(info['user_id'])
                read_user.retweet_count = info['retweet_count']
                read_user.followers = info['followers']
                read_user.influence_score = info['influence_score']
                read_user.favorite_count = info['favorite_count']
                read_user.follower_list = info['follower_list']
                user_dict[info['user_id']] = read_user
        except FileNotFoundError:
            print('Could not find file')
    return user_dict
