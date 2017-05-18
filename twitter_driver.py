# main file to run programs

import networkx as nx
import user
import json
import os
import min_user
import user_stats

# read csv files from specified directory

# directory_to_search = '/home/trent/Documents/School/Spring 2017/CSC 877 Big Data Analysis/CSV Data Politics/'
#directory_to_search = '/home/trent/PycharmProjects/CSC 877 Twitter/1k_data_power_law/fake_users/'

# heroku directory
#directory_to_search = '/app/1k_data/fake_users/'

# write to folder in specified directory
# out_dir = '/home/trent/PycharmProjects/CSC 877 Twitter/gpickle_powerlaw/'
# min_obj_out_dir = '/home/trent/PycharmProjects/CSC 877 Twitter/min_object_scores/'
# test_out_dir = '/home/trent/PycharmProjects/CSC 877 Twitter/test_results/'

# directory_to_search = '/home/trent/PycharmProjects/CSC 877 Twitter/real_data/user_list/'
# follower_dir = '/home/trent/PycharmProjects/CSC 877 Twitter/real_data/follower_list/'
# out_dir = '/home/trent/PycharmProjects/CSC 877 Twitter/real_data/gpickle_powerlaw/'
# min_obj_out_dir = '/home/trent/PycharmProjects/CSC 877 Twitter/real_data/min_object_scores/'
# test_out_dir = '/home/trent/PycharmProjects/CSC 877 Twitter/real_data/test_results/'

# fake data 2
directory_to_search = '/home/trent/PycharmProjects/CSC 877 Twitter/fake_data_2/twitter_users/'
out_dir = '/home/trent/PycharmProjects/CSC 877 Twitter/fake_data_2/gpickle_powerlaw/'
min_obj_out_dir = '/home/trent/PycharmProjects/CSC 877 Twitter/fake_data_2/min_object_scores/'
test_out_dir = '/home/trent/PycharmProjects/CSC 877 Twitter/fake_data_2/test_results/'
user_stats_out = '/home/trent/PycharmProjects/CSC 877 Twitter/fake_data_2/user_stats/'

# tuple for network and it's score
d = {}
g = nx.DiGraph()
network_tuple_list = []
node_count = 0
file_count = 0

def build_network(g, user_object, depth, d):
    global node_count
    d2_score = 0
    d2_count = 0
    d3_score = 0
    d3_count = 0

    min_user_user = min_user.Min_user(user_object.user_id, user_object.influence_score)

    for follower_name in user_object.get_follower_list():\
        # fake data
        follower = read(directory_to_search+follower_name+'.json')

        # real data
        #follower = read(follower_dir + follower_name + '.json')
        min_user_follower = min_user.Min_user(follower.user_id, follower.influence_score)
        g.add_edge(min_user_user, min_user_follower, weight=.1*float(follower.influence_score))
        min_user_object = min_user.Min_user(min_user_follower.user_id, min_user_follower.influence_score)

        node_count += 1
        d2_score += .1*float(min_user_follower.influence_score)
        d2_count += 1

        try:
            with open(min_obj_out_dir + min_user_object.user_id + '.json', 'w+') as outfile:
                json.dump(min_user_object.to_json(), outfile)

        except Exception:
            print('Could not write file min user file: ' + min_user_object.user_id)
        nx.write_gpickle(g, out_dir + user_object.user_id + '.gpickle')
        #for follower_name in user_object.get_follower_list():
        # fake data set
        # follower = read(directory_to_search + follower_name + '.json')
            # real data set
            #follower = read(follower_dir + follower_name + '.json')
        for follower_name_2 in follower.get_follower_list():
            follower_2 = read(directory_to_search + follower_name_2 + '.json')
            min_user_follower_2 = min_user.Min_user(follower_name_2, follower_2.influence_score)
            g.add_edge(min_user_follower, min_user_follower_2, weight=(.1**2*float(follower_2.influence_score)))

            node_count += 1
            d3_score += .1**2*float(follower_2.influence_score)
            d3_count += 1

    return user_stats.User_Stats(user_object, len(g.edges()), d2_score, d3_score, d2_count, d3_count)

def gen_graph_score(user_object):

    d = {}
    g = nx.DiGraph()
    stats_object = build_network(g, user_object, 3, d)
    graph_sum = 0.0
    for edge in g.edges(data=True):
        graph_sum += float(edge[2]['weight'])

    graph_sum += float(user_object.influence_score)
    stats_object.network_score = graph_sum

    min_user_object = min_user.Min_user(user_object.user_id, user_object.influence_score)
    min_user_object.set_network_influence(graph_sum)

    try:
        with open(min_obj_out_dir + min_user_object.user_id + '.json', 'w+') as outfile:
            json.dump(min_user_object.to_json(), outfile)
    except Exception as e:
        print(e)
    try:
        with open(user_stats_out + user_object.user_id + '.json', 'w+') as outfile:
            json.dump(stats_object.to_json(), outfile)
    except Exception as e:
        print(e)

    return graph_sum


def read(file_name):
    try:
        with open(file_name, 'r') as json_data:
            info = json.load(json_data)
            read_user = user.User(info['user_id'])
            read_user.average_retweet_count = info['average_retweet_count']
            read_user.followers_count = info['followers_count']
            read_user.influence_score = info['influence_score']
            read_user.average_favorite_count = info['average_favorite_count']
            read_user.follower_list = info['follower_list']
            return read_user
    except FileNotFoundError:
        print('Could not find file: ' + file_name)

if __name__ == '__main__':
    while True:
        print('======================')
        print('1. Analyze score')
        print('2. Print Analysis')
        print('0. Exit')
        choice = input('Enter choice here: ')
        if choice == '1':
            print('======================')
            print('1. Real data set')
            print('2. Fake data set')
            data_selection = input('Enter data source: ')
            print('== Start Analysis ==')
            for file_name in os.listdir(directory_to_search):
                # file_name = 'user29.json'
                if len(file_name) <= 11 or file_name == 'user100.json':
                    file_count += 1
                    print(str(file_count) + ' : ' + file_name + ' --> Count : ' + str(node_count))
                    user_object = read(directory_to_search + file_name)
                    network_tuple_list.append((user_object.get_user_id(), gen_graph_score(user_object)))

            print("== end ==")
            print('Total nodes: ' + str(node_count))
            network_tuple_list.sort(key=lambda tup: tup[1])
            network_tuple_list.reverse()

            print('== Network Sorted ==')
            print(network_tuple_list)
            with open(test_out_dir + 'results.json', 'w+') as outfile:
                json.dump(dict(network_tuple_list), outfile)
        elif choice == '0':
            quit()
        else:
            print('Please enter the right choice')