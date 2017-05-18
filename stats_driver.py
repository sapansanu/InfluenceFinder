import json
import os
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import math
import read
import user_stats
import user
1
def line_plot(tuple1, tuple2):
    fig = plt.figure(figsize=(10, 6))
    user_list = []
    influence_score = []
    network_score = []

    for elem1, elem2 in tuple1:
        user_list.append(elem1)
        influence_score.append(math.log(float(elem2)))
        network_score.append(math.log(tuple2[search_tuple(elem1, tuple2)][1]))

    plt.bar(range(len(tuple1)), network_score, align='center', color='b')
    plt.bar(range(len(tuple1)), influence_score, align='center', color='r')

    plt.xticks(range(len(tuple1)), user_list, size='small', rotation=90)
    fig.subplots_adjust(bottom=0.29)
    plt.show()


def get_hist(tuple_list):
    array = []
    for item in tuple_list:
        array.append(item[1])
    res = stats.relfreq(array, numbins=75)
    x = res.lowerlimit + np.linspace(0, res.binsize * res.frequency.size, res.frequency.size)
    fig = plt.figure(figsize=(6, 4))
    ax = fig.add_subplot(1, 1, 1)
    ax.bar(x, res.frequency, width=res.binsize)
    plt.show()


# orders the initial influence scores
def order_fake_influence(directory, x):
    file_length = 0
    stop_name = ''
    if int(x) == int(2):
        file_length = 11
        stop_name = 'user100.json'
    elif int(x) == int(3):
        file_length = 12
        stop_name = 'user1000.json'
    synthetic_tuple_list = []
    try:
        # getting individual influence scores and ranking them
        for file_name in os.listdir(directory):
            if len(file_name) <= file_length or file_name == stop_name:
                user_object = read.read(directory + file_name)
                synthetic_tuple_list.append((user_object.user_id, user_object.influence_score))
        synthetic_tuple_list.sort(key=lambda tup: float(tup[1]))
        synthetic_tuple_list.reverse()
    except Exception as e:
        print(e)
    return synthetic_tuple_list


def order_real_influence(directory):
    synthetic_tuple_list = []
    try:
        # getting individual influence scores and ranking them
        for file_name in os.listdir(directory):
            if file_name != 'followers':
                user_object = read.read(directory + file_name)
                synthetic_tuple_list.append((user_object.user_id, user_object.influence_score))
        synthetic_tuple_list.sort(key=lambda tup: float(tup[1]))
        synthetic_tuple_list.reverse()
    except Exception as e:
        print('Exception', e)
    return synthetic_tuple_list


# orders the network stats
def order_network_stats(directory, network_stats_file_name):
    network_tuple_score = []
    try:
        # getting network scores and ranking them
        with open(directory + network_stats_file_name, 'r') as infile_score:
            network_score = json.load(infile_score)

            for key in network_score.keys():
                network_tuple_score.append((key, network_score[key]))
            network_tuple_score.sort(key=lambda tup: float(tup[1]))
            network_tuple_score.reverse()
            return network_tuple_score
    except Exception as e:
        print(e)


# searches tuple and returns rank of the user
def search_tuple(user_id, tuple_to_search):
    for tuple_rank in range(len(tuple_to_search)):
        if tuple_to_search[tuple_rank][0] == user_id:
            return tuple_rank


def read_stats(infile):
    info = json.load(infile)
    temp_user = user.User(info['user_id'])
    temp_user.average_retweet_count = info['average_retweet_count']
    temp_user.followers_count = info['followers_count']
    temp_user.influence_score = info['influence_score']
    temp_user.average_favorite_count = info['average_favorite_count']
    # print(temp_user)
    read_user = user_stats.User_Stats(temp_user,
                                      info['depth_scores'],
                                      info['depth_followers'],
                                      info['network_score'])
    # print(read_user)
    read_user.verified = info['verified']
    read_user.network_score = info['network_score']
    read_user.start_rank = info['start_rank']
    read_user.end_rank = info['end_rank']
    read_user.depth_scores = info['depth_scores']
    read_user.followers = info['followers_count']
    # print(read_user)
    return read_user


def get_followers_vs_network(user_stats_out_directory, test_out_directory):

    fig = plt.figure(figsize=(10, 4))
    user_scores_list_1 = []
    user_scores_list_2 = []
    user_followers_list = []
    user_network_score = []
    user_name = []

    for file in os.listdir(user_stats_out_directory):
        with open(user_stats_out_directory+file, 'r+') as infile:
            user_stat_object = read_stats(infile)
            follower_network = 0
            follower_scores = 0
            for i in range(len(user_stat_object.depth_scores)):
                follower_network += int(user_stat_object.depth_followers[i])
                follower_scores += float(user_stat_object.depth_scores[i])
            user_network_score.append(user_stat_object.network_score)
            user_followers_list.append(follower_network)
            user_scores_list_1.append(user_stat_object.depth_scores[0])
            user_scores_list_2.append(user_stat_object.depth_scores[1])
            user_name.append(int(user_stat_object.user_id[4:]))
    plt.scatter(user_name, user_network_score, 'r') #'r', user_name, user_scores_list_2, 'b')
    plt.show()


def compile_stats_driver(network_stats_file_name, directory_to_search, test_out_directory, user_stats_out_directory, x):
    index = int(x)-1
    influence_scores = []

    if int(x) > 1:
        influence_scores = order_fake_influence(directory_to_search[index], x)
    else:
        influence_scores = order_real_influence(directory_to_search[index])
    network_tuple_scores = order_network_stats(test_out_directory[index], network_stats_file_name)
    total_num_files = len(network_tuple_scores)

    k = input('Enter the top k number of users you want to see ranked: ')
    print('\nOriginal Influence Score')
    for i in range(int(k)):
        print('Rank', i + 1, influence_scores[i])

    print('\nNetwork Score')
    for i in range(int(k)):
        print('Rank', i + 1, network_tuple_scores[i])

    print('\nChange in rank from Influence Network after Network Influence weight was applied')
    total_change = 0
    top_k_change = 0
    for i in range(int(k)):
        post_rank = search_tuple((influence_scores[i][0]), network_tuple_scores)+1
        change = (i+1) - post_rank
        top_k_change += abs(change)
        print((influence_scores[i][0]), 'from rank', i + 1, 'to', post_rank, 'change =', change)
    for i in range(total_num_files):
        total_change += abs((i + 1) - search_tuple((influence_scores[i][0]),
                                                   network_tuple_scores))

    print('\nAverage rank change for top K =', k, 'users:', top_k_change/int(k))
    print('Average rank change for all users:', total_change/total_num_files)
    # generate histogram
    line_plot(influence_scores, network_tuple_scores)
    # # get_followers_vs_network(user_stats_out_directory[index], test_out_directory[index])
    get_hist(network_tuple_scores)
